import os
import sys
import json
from pathlib import Path
from openai import OpenAI

# ---------- Конфигурация ----------
API_KEY = os.getenv("LLM_API_KEY", "queen")
BASE_URL = os.getenv("LLM_API_BASE", "http://10.93.24.167:42005/v1")
MODEL = os.getenv("LLM_MODEL", "qwen3-coder-plus")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Корень проекта (там, где лежит agent.py)
PROJECT_ROOT = Path(__file__).parent.resolve()

# ---------- Безопасная работа с путями ----------
def safe_path(relative_path: str) -> Path:
    """Преобразует относительный путь в абсолютный и проверяет, что он внутри PROJECT_ROOT."""
    requested = (PROJECT_ROOT / relative_path).resolve()
    if not str(requested).startswith(str(PROJECT_ROOT)):
        raise ValueError("Path traversal attempt detected")
    return requested

# ---------- Инструменты ----------
def read_file(path: str) -> str:
    try:
        full = safe_path(path)
        if not full.is_file():
            return f"Error: File not found: {path}"
        return full.read_text(encoding='utf-8')
    except Exception as e:
        return f"Error reading file: {str(e)}"

def list_files(path: str) -> str:
    try:
        full = safe_path(path)
        if not full.is_dir():
            return f"Error: Not a directory: {path}"
        entries = os.listdir(full)
        return "\n".join(entries)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

# ---------- Схемы инструментов для OpenAI ----------
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from the project repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path from project root"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories at a given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative directory path from project root"
                    }
                },
                "required": ["path"]
            }
        }
    }
]

# ---------- Вспомогательная функция для выполнения инструментов ----------
def execute_tool_call(tool_call):
    """Выполняет один tool_call и возвращает результат (строку) и имя вызванной функции."""
    fn_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    if fn_name == "read_file":
        result = read_file(**args)
    elif fn_name == "list_files":
        result = list_files(**args)
    else:
        result = f"Error: unknown tool {fn_name}"
    return result, fn_name, args

# ---------- Основной цикл агента ----------
def agent_loop(user_query: str) -> dict:
    messages = [
        {"role": "system", "content": """You are a helpful assistant with access to the project repository.
You have two tools: read_file and list_files.
- If the user asks about the content of a file (e.g., "How do I resolve a merge conflict?"), you MUST call read_file with the correct path (likely "wiki/git-workflow.md").
- If the user asks to list files in a directory (e.g., "What files are in the wiki?"), you MUST call list_files with that directory path.
- After you receive the result from a tool, you MUST formulate a final answer and stop calling tools. Do not call additional tools after you have the necessary information."""},
        {"role": "user", "content": user_query}
    ]
    all_tool_calls = []
    last_source = None
    max_iterations = 5
    iteration = 0

    while True:
        iteration += 1
        if iteration > max_iterations:
            final_answer = "Error: Agent loop exceeded maximum iterations"
            break

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        assistant_message = response.choices[0].message

        # Добавляем ответ ассистента в историю
        messages.append(assistant_message)

        # Если нет вызовов инструментов — выходим
        if not assistant_message.tool_calls:
            final_answer = assistant_message.content or ""
            break

        # Обрабатываем каждый tool_call
        for tool_call in assistant_message.tool_calls:
            # Выполняем инструмент
            result, fn_name, args = execute_tool_call(tool_call)
            # Сохраняем информацию о вызове
            all_tool_calls.append({
                "name": fn_name,
                "arguments": args
            })
            # Для read_file запоминаем путь как источник
            if fn_name == "read_file":
                last_source = args.get("path")
            # Добавляем результат в сообщения (роль "tool")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return {
        "answer": final_answer,
        "source": last_source,
        "tool_calls": all_tool_calls
    }

# ---------- Точка входа ----------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "What is 2+2?"
    result = agent_loop(query)
    print(json.dumps(result, ensure_ascii=False))