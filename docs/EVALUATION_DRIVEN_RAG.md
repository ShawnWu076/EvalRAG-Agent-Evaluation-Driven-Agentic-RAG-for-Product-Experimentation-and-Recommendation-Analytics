# Evaluation-Driven RAG Plan

EvalRAG uses two complementary evaluation layers.

## 1. Domain-Specific Eval

`scripts/run_eval.py` runs the system against the scenario dataset in `data/eval/eval_questions.jsonl`.

It measures project-specific behavior:

- expected playbook source retrieval;
- concept coverage;
- LLM decision accuracy;
- policy validator corrections and regressions;
- final decision accuracy;
- latency.

This is not Ragas. It is custom evaluation for product experimentation launch decisions.

## 2. Ragas Eval

`scripts/run_ragas_eval.py` consumes saved records from `scripts/run_eval.py --save-records` and computes general RAG quality metrics with Ragas:

- faithfulness: whether the answer is grounded in retrieved context;
- answer relevancy: whether the answer directly addresses the question;
- context precision: whether retrieved contexts are useful and ranked well.

Typical workflow:

```bash
python scripts/run_eval.py --limit 5 --save-records logs/openai_eval_sample5.json
python scripts/run_ragas_eval.py --records logs/openai_eval_sample5.json --limit 5 --output logs/ragas_eval_sample5.json
```

To inspect the prepared Ragas dataset without spending judge tokens:

```bash
python scripts/run_ragas_eval.py --records logs/openai_eval_sample5.json --prepare-only --output logs/ragas_input_sample5.json
```

The Ragas report includes a lightweight failure analysis:

- low context precision -> retrieval failure hypothesis;
- low faithfulness -> hallucination or grounding failure hypothesis;
- low answer relevancy -> answer relevance or reasoning failure hypothesis.

## Golden Dataset Direction

A stronger V1 dataset should move from starter labels to a true golden dataset. Each row should include:

- `id`
- `question`
- `ground_truth` or `reference`
- `expected_sources`
- `expected_concepts`
- `expected_decision`
- `category`
- optional `reference_contexts`

Categories should cover semantic search, launch decision reasoning, negative or unanswerable cases, and eventually CSV/tool-use scenarios.

## LangSmith

LangSmith is not required for the first Ragas integration. It is an observability and tracing layer: it stores traces of each run, including inputs, retrieval steps, LLM calls, outputs, latency, and metadata in a dashboard.

EvalRAG already writes local JSON logs. LangSmith becomes useful when we want hosted trace inspection, collaboration, and experiment comparison. To enable it later, configure:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="your_langsmith_key"
export LANGSMITH_PROJECT="evalrag-agent"
```

Then instrument the RAG pipeline with LangSmith traceable spans for retrieve, generate, policy validation, and evaluation.

## Pre/Post Improvement Loop

The intended evaluation-driven loop is:

```text
Build baseline -> run custom eval + Ragas -> inspect failure report -> improve RAG -> rerun -> compare pre vs post
```

Future work should add a comparison script that reads two reports and shows metric deltas for retrieval, Ragas scores, and decision quality.
