# Local LLM Setup

EvalRAG supports two answer-generation modes:

- `rule`: deterministic local rule/template generator. This is the default and needs no model server.
- `local_llm`: OpenAI-compatible chat completion endpoint, usually served by Ollama or LM Studio.

The retriever, telemetry, evaluation harness, and statistical tools remain deterministic. The LLM only turns retrieved context and tool outputs into a more natural launch memo.

## What the Rule Generator Is

The current `local-rule-generator` is not a language model. It is code in `app/rag_pipeline.py` that:

1. infers a decision label with keyword/tool-output rules,
2. fills a fixed markdown answer template,
3. lists retrieved sources and next steps.

It is closer to "if this scenario pattern appears, choose this decision label and template" than to ChatGPT. This is useful as a stable baseline because evaluation results are repeatable.

## Recommended Local Models

Good starting points for this project:

- `Qwen3-14B` / `qwen3:14b`: strong instruction following, multilingual support, and reasoning/non-reasoning modes. Good first choice for launch memos.
- `Qwen3-8B` / `qwen3:8b`: faster fallback if 14B is too slow.
- `DeepSeek-R1-Distill-Qwen-14B` / `deepseek-r1:14b`: stronger explicit reasoning style, but may produce longer outputs and visible thinking unless configured carefully.

For this project, prefer concise instruct behavior over long chain-of-thought. The prompt already asks the model to return final markdown only.

## Option A: Ollama

Start Ollama and pull a model:

```bash
ollama pull qwen3:14b
```

Run a query with the local LLM backend:

```bash
cd ~/Documents/EvalRAG-Agent
EVALRAG_GENERATOR=local_llm EVALRAG_LLM_BASE_URL=http://localhost:11434/v1 EVALRAG_LLM_MODEL=qwen3:14b EVALRAG_LLM_API_KEY=ollama python3 scripts/query.py "Revenue increased by 5%, but 7-day retention dropped by 2%. Should we launch?" --show-metadata
```

If Ollama is not running or the model is unavailable, EvalRAG falls back to the deterministic rule generator by default and records `generator_backend=rule_fallback` plus `generator_error` in the response/log.

## Already Installed Model Example

On this machine, `ollama list` showed `deepseek-r1:14b` is already installed. You can run EvalRAG with it:

```bash
cd ~/Documents/EvalRAG-Agent
EVALRAG_GENERATOR=local_llm \
EVALRAG_LLM_MODEL=deepseek-r1:14b \
EVALRAG_LLM_BASE_URL=http://localhost:11434/v1 \
EVALRAG_LLM_API_KEY=ollama \
EVALRAG_LLM_TIMEOUT_SECONDS=180 \
.venv/bin/python scripts/query.py "Revenue increased by 5%, but 7-day retention dropped by 2%. Should we launch?" --show-metadata
```

DeepSeek-R1-style reasoning models can be slow for this memo-writing task because they may spend many tokens reasoning before the final answer. For a faster demo, try Qwen3-14B or Qwen3-8B if available.

## Option B: LM Studio

1. Open LM Studio.
2. Download a Qwen3 or DeepSeek R1 Distill GGUF model.
3. Load the model.
4. Go to the Developer tab and start the local server.
5. Use the model id shown by LM Studio.

Typical LM Studio environment:

```bash
cd ~/Documents/EvalRAG-Agent
EVALRAG_GENERATOR=local_llm EVALRAG_LLM_BASE_URL=http://localhost:1234/v1 EVALRAG_LLM_MODEL="<model id from LM Studio>" EVALRAG_LLM_API_KEY=lm-studio python3 scripts/query.py "Revenue increased by 5%, but 7-day retention dropped by 2%. Should we launch?" --show-metadata
```

## FastAPI

Start the API with local LLM generation enabled:

```bash
EVALRAG_GENERATOR=local_llm EVALRAG_LLM_BASE_URL=http://localhost:11434/v1 EVALRAG_LLM_MODEL=qwen3:14b uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Responses include:

- `model`
- `generator_backend`
- `generator_error` when fallback happened

## Future Hosted LLM Path

Because this integration uses an OpenAI-compatible chat-completions shape, the same generator layer can later point to a hosted provider. The rest of the RAG system does not need to change.
