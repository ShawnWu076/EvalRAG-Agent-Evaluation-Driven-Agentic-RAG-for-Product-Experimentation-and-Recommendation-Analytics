# Local LLM Setup

EvalRAG now uses an OpenAI-compatible LLM generator by default. The primary default points to the hosted OpenAI API, and the fallback default points to a local Ollama model:

```text
primary:  https://api.openai.com/v1, gpt-5.4-mini
fallback: http://localhost:11434/v1, qwen3:8b
```

The retriever, telemetry, evaluation harness, and statistical tools remain deterministic. The LLM is responsible for turning retrieved playbook context and tool outputs into a launch memo, including the final decision label.

## Recommended Local Models

Good starting points for this project:

- `Qwen3-8B` / `qwen3:8b`: recommended local fallback for a 16GB M1 Pro because it has a good speed/quality balance.
- `Qwen3-14B` / `qwen3:14b`: stronger but slower.
- `DeepSeek-R1-Distill-Qwen-14B` / `deepseek-r1:14b`: useful for reasoning experiments, but can be slower and more verbose.

For this project, prefer concise instruction-following behavior over long chain-of-thought. The prompt asks the model to return final markdown only.

## Ollama Fallback

Start Ollama and pull the fallback model:

```bash
ollama pull qwen3:8b
```

If the hosted OpenAI call fails and fallback is enabled, EvalRAG tries:

```text
EVALRAG_FALLBACK_LLM_BASE_URL=http://localhost:11434/v1
EVALRAG_FALLBACK_LLM_MODEL=qwen3:8b
EVALRAG_FALLBACK_LLM_TOKEN_PARAMETER=max_tokens
```

A fallback response records:

```text
generator_backend: local_llm_fallback
model: qwen3:8b
generator_error: <primary OpenAI error>
```

## Run Local LLM as Primary

You can also make Ollama the primary backend:

```bash
cd ~/Documents/EvalRAG-Agent
. .venv/bin/activate

EVALRAG_GENERATOR=local_llm \
EVALRAG_LLM_BASE_URL=http://localhost:11434/v1 \
EVALRAG_LLM_MODEL=qwen3:8b \
EVALRAG_LLM_API_KEY=ollama \
EVALRAG_LLM_TOKEN_PARAMETER=max_tokens \
python scripts/query.py "Revenue increased by 5%, but 7-day retention dropped by 2%. Should we launch?" --show-metadata
```

## LM Studio

1. Open LM Studio.
2. Download a Qwen or DeepSeek Distill GGUF model.
3. Load the model.
4. Go to the Developer tab and start the local server.
5. Use the model id shown by LM Studio.

Typical LM Studio environment:

```bash
cd ~/Documents/EvalRAG-Agent
. .venv/bin/activate

EVALRAG_GENERATOR=local_llm \
EVALRAG_LLM_BASE_URL=http://localhost:1234/v1 \
EVALRAG_LLM_MODEL="<model id from LM Studio>" \
EVALRAG_LLM_API_KEY=lm-studio \
EVALRAG_LLM_TOKEN_PARAMETER=max_tokens \
python scripts/query.py "Revenue increased by 5%, but 7-day retention dropped by 2%. Should we launch?" --show-metadata
```

## FastAPI with Local Primary

```bash
EVALRAG_GENERATOR=local_llm \
EVALRAG_LLM_BASE_URL=http://localhost:11434/v1 \
EVALRAG_LLM_MODEL=qwen3:8b \
EVALRAG_LLM_TOKEN_PARAMETER=max_tokens \
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```
