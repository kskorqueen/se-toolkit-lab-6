import os
import json
from openai import OpenAI

# Конфигурация из переменных окружения или значений по умолчанию
API_KEY = os.getenv("LLM_API_KEY", "queen")
BASE_URL = os.getenv("LLM_API_BASE", "http://10.93.24.167:42005/v1")
MODEL = os.getenv("LLM_MODEL", "qwen3-coder-plus")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def ask_llm(prompt: str):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        # Пока tool_calls пуст, в будущем будет расширяться
        result = {
            "answer": answer,
            "tool_calls": []
        }
        return result
    except Exception as e:
        return {
            "error": str(e),
            "answer": None,
            "tool_calls": []
        }

if __name__ == "__main__":
    # Пример: можно передать вопрос через аргумент командной строки
    import sys
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "What is 2+2?"
    output = ask_llm(prompt)
    print(json.dumps(output, ensure_ascii=False))
