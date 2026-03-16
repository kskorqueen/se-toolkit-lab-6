Task 1: LLM Provider and Agent Structure
Choice of LLM Provider and Model
Provider: Locally deployed Qwen Code API via a proxy.

Model: qwen3-coder-plus (available through the proxy).

Endpoint: http://10.93.24.167:42005/v1/chat/completions

API Key: queen (used in the Authorization header).

Agent Structure
The agent will be implemented in the agent.py file. At this stage, it will:

Accept a user query (initially hardcoded in the script or provided via command-line arguments).

Send a request to the LLM through an OpenAI-compatible API.

Receive the response and output it in JSON format with the fields answer and tool_calls (initially tool_calls can be an empty list).

Future work will extend functionality with tools and a knowledge base.
