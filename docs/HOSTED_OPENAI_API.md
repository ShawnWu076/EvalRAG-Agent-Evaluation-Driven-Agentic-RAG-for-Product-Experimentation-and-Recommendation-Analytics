# Hosted OpenAI API Setup

EvalRAG can use the hosted OpenAI API through the same OpenAI-compatible chat-completions layer used for Ollama and LM Studio. Retrieval, statistical tools, telemetry, and evaluation stay the same; only the answer generator changes.

## 1. Set Your API Key

Use an environment variable instead of committing keys to the repo:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Do not put real API keys in `.env.example`, README, screenshots, or Git commits.

## 2. Run One Query

```bash
cd ~/Documents/EvalRAG-Agent
. .venv/bin/activate

EVALRAG_GENERATOR=openai_compatible \
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1 \
EVALRAG_LLM_MODEL=gpt-5.4-mini \
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens \
python scripts/query.py "Revenue increased by 5%, but 7-day retention dropped by 2%. Should we launch?" --show-metadata
```

Expected metadata:

```text
model: gpt-5.4-mini
generator_backend: openai_compatible
```

## 3. Run CSV Analysis

```bash
EVALRAG_GENERATOR=openai_compatible \
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1 \
EVALRAG_LLM_MODEL=gpt-5.4-mini \
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens \
python scripts/analyze_csv.py data/synthetic/guardrail_failure.csv --show-tools
```

## 4. Run a Small Eval First

API eval costs money because each eval question calls the model. Start with a small limit:

```bash
EVALRAG_GENERATOR=openai_compatible \
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1 \
EVALRAG_LLM_MODEL=gpt-5.4-mini \
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens \
python scripts/run_eval.py --limit 5 --save-records logs/openai_eval_sample5.json
```

Then inspect:

```bash
cat logs/openai_eval_sample5.json
```

Run the full 25-question eval only after the sample looks good:

```bash
EVALRAG_GENERATOR=openai_compatible \
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1 \
EVALRAG_LLM_MODEL=gpt-5.4-mini \
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens \
python scripts/run_eval.py --save-records logs/openai_eval_full.json
```

## Notes

- The project currently uses Chat Completions for compatibility with local model servers.
- OpenAI recommends the newer Responses API for new projects, but Chat Completions is still a practical compatibility layer here because Ollama, LM Studio, and OpenAI can share the same request shape.
- The hosted model can be changed with `EVALRAG_LLM_MODEL`.
- `EVALRAG_LLM_API_KEY` takes precedence over `OPENAI_API_KEY`; if it is unset, EvalRAG reads `OPENAI_API_KEY`.
