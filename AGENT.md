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
