# EvalRAG Agent

Evaluation-driven agentic RAG for product experimentation and recommendation analytics.

EvalRAG Agent turns product experiment questions into structured, source-grounded launch memos. It retrieves from a small experimentation playbook, calls an OpenAI-compatible LLM to synthesize the answer and decision label, logs retrieved chunks and scores, evaluates answer quality, and can summarize synthetic A/B test CSVs with statistical tools.

## What This Project Demonstrates

- RAG over a domain playbook instead of a generic PDF chatbot.
- Hybrid retrieval with BM25 plus hashed-vector scoring.
- LLM-generated launch memos with explicit, parseable decision labels.
- Telemetry for query, retrieved chunks, scores, latency, and answer.
- Evaluation harness for source hit rate, source match rate, all-sources-found rate, top-1 source match, source precision@K, concept coverage, decision accuracy, and MRR.
- Agentic extension with SRM checks, metric lifts, significance approximations, and segment analysis over CSV data.

## Why Evaluation-Driven RAG

Naive RAG demos often work on cherry-picked questions but fail when retrieval returns irrelevant chunks, important source documents are missed, or the model generates unsupported answers. This project is built around a different question:

```text
Did the system calculate the facts correctly, retrieve the right rules, and make a reasonable recommendation based on those rules?
```

The goal is not only to produce a plausible answer. The goal is to make the RAG system inspectable, measurable, and improvable.

EvalRAG evaluates three failure modes:

1. **Retrieval failure**

   Did the system retrieve the right playbook sections?

   Example metrics:

   - Hit@K
   - Source match rate
   - All expected sources found rate
   - Top-1 source match rate
   - Source precision@K
   - Mean reciprocal rank

2. **Grounding / reasoning failure**

   Did the answer use the retrieved rules, or did it invent unsupported claims?

   Example checks:

   - Concept coverage
   - Faithfulness / groundedness
   - Retrieved-source inspection

3. **Decision failure**

   Did the final recommendation match the experiment scenario?

   Example decision labels:

   - `launch`
   - `investigate_further`
   - `partial_rollout`
   - `do_not_trust_result`
   - `use_did_or_quasi_experiment`

This turns the development loop from vibe-based prompting into:

```text
Build -> Log -> Evaluate -> Diagnose -> Optimize
```

## Repository Layout

```text
app/
  main.py                    FastAPI app
  rag_pipeline.py            retrieval, memo generation, telemetry orchestration
  retrieval.py               markdown chunking + hybrid retriever
  telemetry.py               JSONL logging
  tools/
    experiment_stats.py      SRM, lift, tests, segment analysis
    data_validation.py       CSV validation and metric inference
data/
  playbook/                  domain knowledge base
  eval/eval_questions.jsonl  scenario-based evaluation set
  synthetic/                 generated experiment CSVs
scripts/
  build_index.py
  run_eval.py
  compare_retrievers.py
  generate_synthetic_data.py
logs/
  rag_logs.jsonl             created at runtime
docs/
  LOCAL_LLM.md               Ollama / LM Studio setup
  HOSTED_OPENAI_API.md       Hosted OpenAI API setup
tests/
```

## Quick Start

The core build/eval/stat scripts are dependency-light and run with the Python standard library.

```bash
python3 scripts/build_index.py
export OPENAI_API_KEY="your_api_key_here"
python3 scripts/query.py "Revenue increased but 7-day retention dropped. Should we launch?" --show-metadata
python3 scripts/analyze_csv.py data/synthetic/guardrail_failure.csv --show-tools
python3 scripts/run_eval.py
python3 scripts/compare_retrievers.py
python3 scripts/generate_synthetic_data.py
python3 -m unittest discover -s tests -p 'test*.py' -v
```

To run the FastAPI service:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build_index.py
uvicorn app.main:app --reload
```

Then call:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Revenue increased but 7-day retention dropped. Should we launch?"}'
```

## LLM Generation

By default, EvalRAG uses an OpenAI-compatible LLM generator. The primary default points to the hosted OpenAI API, and the fallback default points to local Ollama with `qwen3:8b`. Keep your hosted key in an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"

EVALRAG_GENERATOR=openai_compatible \
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1 \
EVALRAG_LLM_MODEL=gpt-5.4-mini \
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens \
python3 scripts/query.py "Revenue increased but 7-day retention dropped. Should we launch?" --show-metadata
```

For API-based eval, start small to inspect quality and cost:

```bash
EVALRAG_GENERATOR=openai_compatible \
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1 \
EVALRAG_LLM_MODEL=gpt-5.4-mini \
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens \
python3 scripts/run_eval.py --limit 5 --save-records logs/openai_eval_sample5.json
```

See `docs/HOSTED_OPENAI_API.md` for details.

## Example V1 Question

```text
We tested a new recommendation ranking model.
Revenue increased by 5%, CTR increased by 7%, but 7-day retention dropped by 2%.
Should we launch?
```

Expected behavior:

- Retrieve `guardrail_metrics.md`, `launch_decision.md`, and `recommendation_experiments.md`.
- Recommend `investigate_further`.
- Explain that retention is a guardrail metric.
- Suggest statistical checks, segment analysis, and partial rollout only if downside is isolated.

## Example V2 CSV Flow

Generate synthetic data:

```bash
python3 scripts/generate_synthetic_data.py
```

Use the API:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "question=Should we launch this recommendation experiment?" \
  -F "file=@data/synthetic/guardrail_failure.csv"
```

The response includes the launch memo plus `tool_summary` with SRM, metric lifts, approximate tests, and segment summaries.

## Evaluation

The scenario dataset lives at `data/eval/eval_questions.jsonl`.

Each record can include:

- `expected_sources`
- `expected_concepts`
- `expected_decision`

Run:

```bash
python3 scripts/run_eval.py --top-k 5
```

Compare retrieval settings without calling an LLM:

```bash
python3 scripts/compare_retrievers.py
```

Run retrieval-only eval when you want to debug search quality without generation cost:

```bash
python3 scripts/run_eval.py --retrieval-only
```

The goal is to make quality visible:

```text
Build -> Log -> Evaluate -> Diagnose -> Optimize
```

## Notes

The deterministic memo generator has been removed. The current pipeline expects an OpenAI-compatible LLM endpoint, extracts the final decision label from the generated memo, and falls back to local `qwen3:8b` when the hosted call fails and Ollama is available.
