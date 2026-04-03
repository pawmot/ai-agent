## Requirements
- Python 3.12+
- uv

## Setup

```bash
uv sync
source .venv/bin/activate
```

Copy `.env.example` to `.env` and add your API keys.

## Run

**Anthropic (claude-haiku-4-5):**
```bash
uv run single_litellm.py "your prompt here"
```

**Google Gemini (gemini-2.5-flash):**
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
