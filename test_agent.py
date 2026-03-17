import subprocess
import json
import sys


def test_agent():
    """Test basic agent functionality with default question."""
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


def test_framework_question_uses_read_file():
    """Test that agent uses read_file tool for framework question."""
    result = subprocess.run(
        [sys.executable, "agent.py", "What Python web framework does this project's backend use?"],
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0, f"Agent failed with error: {result.stderr}"

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, f"Output is not valid JSON: {result.stdout}"

    # Check that answer mentions FastAPI
    assert "fastapi" in output["answer"].lower(), "Answer should mention FastAPI"

    # Check that read_file was used
    tools_used = [tc.get("tool") for tc in output.get("tool_calls", [])]
    assert "read_file" in tools_used, f"Expected read_file tool, got: {tools_used}"

    # Check that source field is set
    assert output.get("source"), "Source field should be set for code questions"

    print("Test passed: framework question uses read_file!")


def test_items_count_uses_query_api():
    """Test that agent uses query_api tool for data-dependent questions."""
    result = subprocess.run(
        [sys.executable, "agent.py", "How many items are currently stored in the database?"],
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0, f"Agent failed with error: {result.stderr}"

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, f"Output is not valid JSON: {result.stdout}"

    # Check that answer contains a number
    import re
    numbers = re.findall(r'\d+', output["answer"])
    assert len(numbers) > 0, "Answer should contain a number"

    # Check that query_api was used
    tools_used = [tc.get("tool") for tc in output.get("tool_calls", [])]
    assert "query_api" in tools_used, f"Expected query_api tool, got: {tools_used}"

    print("Test passed: items count question uses query_api!")


if __name__ == "__main__":
    test_agent()
    test_framework_question_uses_read_file()
    test_items_count_uses_query_api()
    print("\nAll tests passed!")