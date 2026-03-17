# Agent Documentation

## Overview
This agent uses a locally deployed Qwen Code API proxy to answer user queries. It is implemented in `agent.py` and communicates with the LLM via an OpenAI-compatible interface.

## LLM Provider
- **Provider**: Custom proxy based on Qwen Code.
- **Model**: `qwen3-coder-plus`
- **API Base URL**: `http://10.93.24.167:42005/v1`
- **API Key**: `queen` (set via environment variable `LLM_API_KEY`)

## How to Run
1. Ensure you have Python 3.8+ and install dependencies:
   ```bash
   pip install openai
## Tools
The agent now supports two tools for accessing the project repository:

- `read_file(path)`: reads a file and returns its content.
- `list_files(path)`: lists entries in a directory.

Both tools are protected against path traversal attacks: any request to a path outside the project root is rejected.

## Agentic Loop
The agent performs a multi-step loop:
1. Sends the user query along with the tool definitions.
2. If the LLM requests tool calls, they are executed and their results are fed back.
3. The loop continues until a final answer without tool calls is received.

## Output Format
The agent returns a JSON object with:
- `answer`: the final answer.
- `source`: the path of the last file read (if any), otherwise `null`.
- `tool_calls`: an array of all tool invocations (each with `name` and `arguments`).
## Task 3: System Agent

### New Tool: `query_api`
The agent now can interact with the live backend API using the `query_api` tool. It sends HTTP requests with the configured `LMS_API_KEY` and returns the status code and response body. The base URL is set via `AGENT_API_BASE_URL` (default `http://localhost:42002`). This allows the agent to answer questions about runtime data, such as item counts, error responses, and endpoint behavior.

### Tool Selection Strategy
The system prompt has been extended to guide the LLM:
- Use `read_file` for documentation and source code.
- Use `list_files` for exploring directories.
- Use `query_api` for live data from the backend.

After receiving a tool result, the agent is instructed to stop calling further tools unless a multi-step diagnosis is needed (e.g., query an API, then read the source to explain an error).

### Benchmark Results
After several iterations, the agent passed all 10 local evaluation questions. The most challenging were those requiring combining `query_api` with `read_file` to diagnose bugs (e.g., questions 6 and 7). Improving the tool descriptions and adding examples in the prompt resolved these issues. The final score on the local benchmark is 10/10.

### Lessons Learned
- Precise tool descriptions are crucial: the LLM needs to know exactly what each tool does and when to use it.
- For multi-step tasks, the prompt must explicitly allow sequential tool calls.
- Error handling in `query_api` must return structured information so the LLM can interpret failures.
- Using environment variables for all configuration ensures the agent works with the autochecker's settings.
