## Requirements
- Python 3.12+
- uv

## Setup

```bash
uv sync
```

Copy `.env.example` to `.env` and add your API keys.

## Run

1. **Anthropic (claude-haiku-4-5) with MCP support**
First install dependencies for the add MCP server:
```bash
cd mcp_servers/add
uv sync
cd -
```
Then run the power mcp in a separate shell (or move it to background like below)
```bash
cd mcp_servers/power
uv sync
uv run main.py &
cd -
```
Then
```bash
uv run single_litellm_with_mcp.py "Compute (a) 2 + 5, (b) 5 to the power of 3"
```
2. **Anthropic (claude-haiku-4-5):**
```bash
uv run single_litellm.py "your prompt here"
```

3. **Google Gemini (gemini-2.5-flash):**
```bash
uv run single_genai.py "your prompt here"
```

Add `--verbose` to either command to see token usage and tool call details.

The agent operates on the `calculator/` directory — it can read, write, and execute files there. It won't be able to break out of that sandbox.

## Switching models in single_litellm.py

LiteLLM supports many providers. Change the `model` argument in `single_litellm.py`. To check the list of supported models check [LiteLLM providers page](https://docs.litellm.ai/docs/providers). Remember about adding the corresponding API key to `.env` file if not already there.


## Example

Change the precedence of + operator to 3 in `calculator/pkg/calculator.py`, then run:

```bash
uv run single_litellm.py "The calculator returns wrong results. Confirm, fix, test and report to me the cause of the problem."
```

## Development

For development remember about virtual environment activation in your IDE.
