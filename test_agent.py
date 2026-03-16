import subprocess
import json
import sys

def test_agent():
    # Запускаем agent.py без аргументов (использует вопрос по умолчанию)
    result = subprocess.run(
        [sys.executable, "agent.py"],
        capture_output=True,
        text=True,
        timeout=10
    )
    assert result.returncode == 0, f"Agent failed with error: {result.stderr}"
    
    # Парсим stdout как JSON
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, f"Output is not valid JSON: {result.stdout}"
    
    # Проверяем наличие обязательных полей
    assert "answer" in output, "Missing 'answer' field"
    assert "tool_calls" in output, "Missing 'tool_calls' field"
    
    # Дополнительно можно проверить, что answer не пустой
    assert output["answer"] is not None, "Answer is None"
    
    print("Test passed!")

if __name__ == "__main__":
    test_agent()