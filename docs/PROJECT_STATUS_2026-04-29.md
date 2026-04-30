# EvalRAG Agent Project Status - 2026-04-29

This note is a handoff document for continuing the project tomorrow.

## What This Project Is Right Now

This is a working **EvalRAG Agent prototype**.

It is not a production-grade system yet, but it is also not an empty presentation project. The repository already has:

- A product experimentation and recommendation analytics playbook.
- A locally runnable RAG pipeline for retrieval and structured launch memo generation.
- An evaluation harness for measuring retrieval and decision quality.
- A V2-style agentic path that reads synthetic experiment CSVs, calls statistical tools, and generates a launch memo.
- FastAPI endpoints, CLI demos, Docker config, tests, and a README.

In short: this is a **functional prototype / MVP**. The next phase is to make it more realistic, more robust, and more polished for GitHub, resume, and interview use.

## What Was Built Today

1. Created the project structure:
   - `app/`
   - `data/playbook/`
   - `data/eval/`
   - `data/synthetic/`
   - `scripts/`
   - `tests/`
   - `docs/`

2. Wrote the domain playbook:
   - `ab_testing.md`
   - `guardrail_metrics.md`
   - `launch_decision.md`
   - `recommendation_experiments.md`
   - `ads_experiments.md`
   - `marketplace_metrics.md`
   - `sample_ratio_mismatch.md`
   - `segment_analysis.md`
   - `did_policy_analysis.md`
   - `experiment_telemetry.md`

3. Implemented V1 RAG:
   - Markdown document loading
   - Heading-aware chunking
   - BM25 + hashed-vector hybrid retrieval
   - Structured launch memo generation
   - Retrieved source display
   - JSONL telemetry logging

4. Implemented the evaluation harness:
   - `data/eval/eval_questions.jsonl`
   - `scripts/run_eval.py`
   - `scripts/compare_retrievers.py`
   - Metrics: source hit rate, source match rate, MRR, concept coverage, decision accuracy, latency

5. Implemented the V2 statistical-tool prototype:
   - SRM check
   - Metric lift calculation
   - Approximate t-test
   - Two-proportion z-test
   - Segment analysis
   - Experiment summary generation

6. Generated synthetic experiment CSV scenarios:
   - Clean win
   - Guardrail failure
   - SRM failure
   - CTR up / CVR down
   - Segment harm

7. Added demo entry points:
   - `scripts/query.py`
   - `scripts/analyze_csv.py`
   - FastAPI `/ask`
   - FastAPI `/analyze`

8. Added tests:
   - Pipeline decision routing
   - SRM classification
   - Metric lift calculation

## Verification Results

The following commands were run successfully:

```bash
python3 scripts/build_index.py
python3 -m unittest
python3 scripts/run_eval.py
python3 scripts/compare_retrievers.py
python3 scripts/query.py "Revenue increased but 7-day retention dropped. Should we launch?"
python3 scripts/analyze_csv.py data/synthetic/guardrail_failure.csv --show-tools
```

Current evaluation result on the starter eval set:

```text
question_count: 25
source_hit_at_k: 1.0
source_match_rate: 0.6733
mean_reciprocal_rank: 0.93
concept_coverage: 0.7733
decision_accuracy: 1.0
```

Important caveat: this is a small starter evaluation set. These numbers should not be treated as final system quality. The next step is to expand the evaluation set to 80-100 scenarios.

## How To Continue Tomorrow

Go to the project directory:

```bash
cd ~/Documents/EvalRAG-Agent
```

If the directory has not been renamed yet, use the current directory:

```bash
cd "/Users/alex_z/Documents/New project 2"
```

Build the playbook index:

```bash
python3 scripts/build_index.py
```

Ask a single natural-language question:

```bash
python3 scripts/query.py "A new recommendation model increased revenue by 5% but 7-day retention dropped by 2%. Should we launch?"
```

Generate synthetic CSVs:

```bash
python3 scripts/generate_synthetic_data.py
```

Run the CSV-based agentic analysis:

```bash
python3 scripts/analyze_csv.py data/synthetic/guardrail_failure.csv --show-tools
```

Run evaluation:

```bash
python3 scripts/run_eval.py
```

Compare retrievers:

```bash
python3 scripts/compare_retrievers.py
```

Run tests:

```bash
python3 -m unittest
```

## How To Run FastAPI

First-time API setup:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build_index.py
uvicorn app.main:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

Test `/ask`:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Revenue increased but 7-day retention dropped. Should we launch?"}'
```

Test `/analyze`:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "question=Should we launch this recommendation experiment?" \
  -F "file=@data/synthetic/guardrail_failure.csv"
```

## What Still Needs Improvement

1. Add a real LLM generation path:
   - Historical note: the initial prototype used a deterministic memo fallback; the current pipeline uses an OpenAI-compatible LLM with local Qwen fallback.
   - Next, add an optional OpenAI-powered generator using retrieved chunks and tool outputs.

2. Add real embeddings and a vector database:
   - The current retriever uses dependency-light hashed vectors.
   - Next, add OpenAI embeddings plus FAISS or Chroma.

3. Expand the evaluation dataset:
   - The current eval set has 25 starter questions.
   - For a stronger portfolio project, expand this to 80-100 scenarios.

4. Add faithfulness evaluation:
   - Current evaluation covers source matching, concepts, and decision labels.
   - Add LLM-as-judge, Ragas, DeepEval, or a manual rubric for groundedness.

5. Improve statistical rigor:
   - The current tests use dependency-light approximations.
   - Add SciPy for Welch t-tests, confidence intervals, proportion tests, and multiple-testing warnings.

6. Build a demo UI:
   - Streamlit is fastest.
   - A React/FastAPI UI would look more polished.
   - Useful panels: question input, CSV upload, answer, retrieved sources, tool summary, telemetry.

7. Complete the error-analysis notebook:
   - The current notebook is a placeholder.
   - Add analysis for failed eval cases, missed sources, concept gaps, and retrieval comparisons.

8. Improve the GitHub presentation:
   - Add an architecture diagram.
   - Add before/after retrieval comparison tables.
   - Add screenshots or a short demo GIF.
   - Add resume bullets and interview explanation.

## Recommended Next Steps

1. Polish the README so the GitHub landing page looks complete.
2. Expand `eval_questions.jsonl` from 25 to 50 questions.
3. Add an optional OpenAI LLM generator while keeping the local fallback.
4. Add a Streamlit demo or simple frontend.
5. Add a retrieval comparison table to the README.

## One-Sentence Project Pitch

I built a working prototype of an evaluation-driven agentic RAG system for product experimentation analytics. It retrieves from a custom experimentation playbook, generates structured launch memos, logs retrieval traces, evaluates retrieval and decision quality, and includes an agentic CSV analysis path with SRM, lift, significance, and segment tools.

