import subprocess
import json
import sys

def test_read_file_tool_framework():
    result = subprocess.run(
        [sys.executable, "agent.py", "What Python web framework does this project's backend use?"],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0, f"Agent failed: {result.stderr}"
    output = json.loads(result.stdout)
    assert "tool_calls" in output
    tool_calls = output["tool_calls"]
    # Ищем по ключу "tool" (а не "name")
    assert any(tc.get("tool") == "read_file" for tc in tool_calls), "read_file not called"
    print("test_read_file_tool_framework passed")

def test_query_api_tool_items():
    result = subprocess.run(
        [sys.executable, "agent.py", "How many items are in the database?"],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0, f"Agent failed: {result.stderr}"
    output = json.loads(result.stdout)
    assert "tool_calls" in output
    tool_calls = output["tool_calls"]
    # Проверяем наличие query_api
    assert any(tc.get("tool") == "query_api" for tc in tool_calls), "query_api not called"
    # Дополнительно проверяем аргументы
    for tc in tool_calls:
        if tc.get("tool") == "query_api":
            args = tc.get("args", {})
            assert args.get("method") == "GET", f"Expected GET, got {args.get('method')}"
            assert args.get("path") == "/items/", f"Expected /items/, got {args.get('path')}"
            break
    print("test_query_api_tool_items passed")

if __name__ == "__main__":
    test_read_file_tool_framework()
    test_query_api_tool_items()
    print("All Task 3 tests passed!")