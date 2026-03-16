

import subprocess
import json
import sys

def test_read_file_tool():
    """Вопрос, требующий чтения файла wiki/git-workflow.md"""
    result = subprocess.run(
        [sys.executable, "agent.py", "How do you resolve a merge conflict?"],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0, f"Agent failed: {result.stderr}"
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, f"Invalid JSON: {result.stdout}"
    
    assert "answer" in output
    assert "source" in output
    assert "tool_calls" in output
    
    tool_calls = output["tool_calls"]
    # Проверяем, что был вызов read_file
    assert any(tc.get("name") == "read_file" for tc in tool_calls), "read_file not called"
    # Проверяем source
    assert output["source"] == "wiki/git-workflow.md", f"Expected source wiki/git-workflow.md, got {output['source']}"
    print("test_read_file_tool passed")

def test_list_files_tool():
    """Вопрос, требующий листинга директории wiki"""
    result = subprocess.run(
        [sys.executable, "agent.py", "What files are in the wiki?"],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0, f"Agent failed: {result.stderr}"
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, f"Invalid JSON: {result.stdout}"
    
    assert "tool_calls" in output
    tool_calls = output["tool_calls"]
    assert any(tc.get("name") == "list_files" for tc in tool_calls), "list_files not called"
    print("test_list_files_tool passed")

if __name__ == "__main__":
    test_read_file_tool()
    test_list_files_tool()
    print("All tests passed!")
