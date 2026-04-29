# EvalRAG Agent

Evaluation-driven agentic RAG for product experimentation and recommendation analytics.

EvalRAG Agent turns product experiment questions into structured, source-grounded launch memos. It retrieves from a small experimentation playbook, logs retrieved chunks and scores, evaluates answer quality, and can summarize synthetic A/B test CSVs with statistical tools.

## What This Project Demonstrates

- RAG over a domain playbook instead of a generic PDF chatbot.
- Hybrid retrieval with BM25 plus hashed-vector scoring.
- Structured launch memos with explicit decision labels.
- Telemetry for query, retrieved chunks, scores, latency, and answer.
- Evaluation harness for source hit rate, source match rate, concept coverage, decision accuracy, and MRR.
- Agentic extension with SRM checks, metric lifts, significance approximations, and segment analysis over CSV data.

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
tests/
```

## Quick Start

The core build/eval/stat scripts are dependency-light and run with the Python standard library.

```bash
python3 scripts/build_index.py
python3 scripts/query.py "Revenue increased but 7-day retention dropped. Should we launch?"
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

Compare retrieval settings:

```bash
python3 scripts/compare_retrievers.py
```

The goal is to make quality visible:

```text
Build -> Log -> Evaluate -> Diagnose -> Optimize
```

## Notes

The default answer generator is deterministic so the project can run without an LLM key. In a production version, replace or augment `generate_structured_answer()` with an LLM call using the same retrieved chunks, tool outputs, output schema, and telemetry record.
