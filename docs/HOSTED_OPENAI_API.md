# Hosted OpenAI API Setup

EvalRAG can use the hosted OpenAI API through the same OpenAI-compatible chat-completions layer used for Ollama and LM Studio. Retrieval, statistical tools, telemetry, and evaluation stay the same; the primary answer generator is the hosted model by default.

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

If the hosted call fails but Ollama is running with `qwen3:8b`, metadata will show `generator_backend: local_llm_fallback`.

## 3. Run CSV Analysis

```bash
EVALRAG_GENERATOR=openai_compatible \
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1 \
EVALRAG_LLM_MODEL=gpt-5.4-mini \
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens \
python scripts/analyze_csv.py data/synthetic/guardrail_failure.csv --show-tools
```

## 4. Run the 25-Question Eval

API eval costs money because each eval question calls the model. The current eval set has 25 questions, so the default command runs the full set:

```bash
EVALRAG_GENERATOR=openai_compatible \
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1 \
EVALRAG_LLM_MODEL=gpt-5.4-mini \
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens \
python scripts/run_eval.py --save-records logs/openai_eval_full.json
```

Inspect the saved records:

```bash
cat logs/openai_eval_full.json
```

Optional strict concept judging adds extra LLM calls only for unresolved concept gaps:

```bash
EVALRAG_GENERATOR=openai_compatible \
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1 \
EVALRAG_LLM_MODEL=gpt-5.4-mini \
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens \
python scripts/run_eval.py --concept-judge --save-records logs/openai_eval_judge_full.json
```

You can use a separate judge model with `EVALRAG_CONCEPT_JUDGE_MODEL`; otherwise it uses the main LLM model.

For Ragas judge calls, `scripts/run_ragas_eval.py` defaults to `gpt-5.4-mini`, `text-embedding-3-small`, `EVALRAG_RAGAS_MAX_TOKENS=4096`, and conservative timeout/concurrency settings to avoid truncated structured judge outputs.

## Notes

- The project currently uses Chat Completions for compatibility with local model servers.
- OpenAI recommends the newer Responses API for new projects, but Chat Completions is still a practical compatibility layer here because Ollama, LM Studio, and OpenAI can share the same request shape.
- The hosted model can be changed with `EVALRAG_LLM_MODEL`.
- `EVALRAG_LLM_API_KEY` takes precedence over `OPENAI_API_KEY`; if it is unset, EvalRAG reads `OPENAI_API_KEY`.
