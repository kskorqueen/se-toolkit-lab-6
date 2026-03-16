# Task 2: Adding Tools for File Access

## Tool Schemas
We will define two tools using OpenAI's function-calling format:

- **read_file**: reads a file from the project repository.  
  Parameters: `path` (string, relative from project root).  
  Returns: file contents or error message.  
- **list_files**: lists files and directories in a given path.  
  Parameters: `path` (string, relative from project root).  
  Returns: newline-separated list of entries or error.

## Security: Path Traversal Prevention
Both tools will normalize the requested path against the project root (`PROJECT_ROOT = Path(__file__).parent.resolve()`). If the resolved absolute path does not start with the project root, an error is raised. This prevents `../` attacks.

## Agentic Loop Implementation
The agent will:
1. Send the user query along with the tool definitions.
2. If the LLM response contains `tool_calls`, execute each tool with the provided arguments, collect results, and append them as `tool` messages.
3. Repeat until a final assistant message (without `tool_calls`) is received.
4. Extract the final answer and collect all tool calls (name and arguments) into the `tool_calls` field. The `source` field will contain the path of the last `read_file` call, if any.

## JSON Output Format
The agent outputs a JSON object with:
- `answer`: the final answer from the LLM.
- `source`: path of the file used (if any), otherwise `null`.
- `tool_calls`: list of tool invocation objects (each with `name` and `arguments`).
