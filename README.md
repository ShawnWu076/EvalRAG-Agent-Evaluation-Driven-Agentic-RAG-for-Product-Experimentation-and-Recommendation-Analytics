# EvalRAG Agent

Evaluation-driven agentic RAG for product experimentation analytics.

EvalRAG Agent is a prototype experiment-analysis copilot that turns product experiment questions and synthetic A/B test CSVs into structured, source-grounded launch memos. It retrieves from a domain playbook, calls an OpenAI-compatible LLM to synthesize the answer and decision label, logs retrieval traces, evaluates quality, and can run lightweight statistical tools for experiment diagnostics.

The project is intentionally not just another "chatbot over docs." The main idea is to make an AI-assisted launch recommendation system inspectable, measurable, and improvable.

## Motivation

A general-purpose LLM can often answer a question like:

```text
Revenue increased, but retention dropped. Should we launch?
```

But in real product experimentation work, a plausible answer is not enough. The system should answer based on the team's playbook, the available experiment data, and explicit evidence. It should also make failures visible:

- Did retrieval find the right playbook sections?
- Did the answer use retrieved evidence instead of inventing unsupported rules?
- Did the statistical tools calculate experiment facts correctly?
- Did the final launch recommendation match the scenario?
- Can we inspect the retrieved chunks, scores, decision label, latency, and model used?

EvalRAG turns RAG development from vibe-based prompting into:

```text
Build -> Log -> Evaluate -> Diagnose -> Optimize
```

## Current Scope

Current focus: product experimentation analytics.

The system supports scenarios such as:

- Revenue improved, but retention declined.
- CTR improved, but conversion quality dropped.
- Sample ratio mismatch makes an experiment untrustworthy.
- A launch looks good overall but harms an important segment.
- A rollout was non-randomized and should use DiD or another quasi-experimental design.
- A CSV experiment needs SRM checks, metric lifts, significance approximations, and segment summaries.

This is still a prototype, not a production launch-decision system. The goal is to demonstrate a measurable architecture that can be iterated toward a more mature human-in-the-loop experimentation copilot.

## What This Project Demonstrates

- RAG over a product experimentation playbook instead of a generic PDF chatbot.
- Hybrid retrieval using BM25 plus hashed-vector scoring.
- LLM-generated launch memos with explicit, parseable decision labels.
- Hybrid decision tracing with `llm_decision`, `policy_decision`, and `final_decision`.
- Hosted OpenAI-compatible generation by default, with local Ollama `qwen3:8b` fallback.
- Telemetry for query, retrieved chunks, scores, latency, answer, model, and backend.
- Evaluation harness for retrieval quality, concept coverage, decision accuracy, and latency.
- Retrieval-only eval mode for debugging search quality without LLM cost.
- CSV analysis tools for SRM checks, metric lifts, approximate tests, and segment analysis.

## Architecture

```text
User question / CSV
        |
        v
Hybrid Retriever over playbook chunks
        |
        v
Statistical tools, when CSV is provided
        |
        v
OpenAI-compatible LLM generator
        |
        v
LLM memo + llm_decision
        |
        v
Policy validator
        |
        v
Final launch memo + final_decision
        |
        v
Telemetry log + evaluation metrics
```

The LLM is responsible for synthesizing the answer and choosing one decision label from the allowed decision set. The code then parses that label, validates it against hard product-experiment policies, and evaluates both the LLM proposal and final decision against the scenario dataset.

Allowed decision labels:

- `launch`
- `do_not_launch`
- `investigate_further`
- `partial_rollout`
- `do_not_trust_result`
- `use_did_or_quasi_experiment`

## Repository Layout

```text
app/
  main.py                    FastAPI app
  rag_pipeline.py            RAG orchestration, LLM generation, policy validation, eval helpers
  policy_validator.py        Hard-constraint policy checks for hybrid decisions
  llm_generator.py           OpenAI-compatible chat-completions client and prompt builder
  retrieval.py               BM25 + hashed-vector hybrid retriever
  chunking.py                Markdown playbook chunking and index persistence
  telemetry.py               JSONL logging
  tools/
    experiment_stats.py      SRM, lift, tests, segment analysis
    data_validation.py       CSV validation and metric inference
data/
  playbook/                  Product experimentation playbook
  eval/eval_questions.jsonl  Scenario-based evaluation set
  synthetic/                 Synthetic experiment CSVs
scripts/
  build_index.py             Rebuild playbook chunk index
  query.py                   Ask one question from CLI
  analyze_csv.py             Analyze one synthetic experiment CSV
  run_eval.py                Run scenario evaluation
  compare_retrievers.py      Compare retrieval settings without LLM calls
  generate_synthetic_data.py Generate synthetic CSV scenarios
docs/
  HOSTED_OPENAI_API.md       Hosted OpenAI setup
  LOCAL_LLM.md               Ollama / LM Studio setup
  DECISION_EVALUATION.md     LLM/policy/final decision tracing
logs/                        Runtime logs and saved eval records, ignored by git
tests/                       Unit tests
```

## Setup

```bash
cd ~/Documents/EvalRAG-Agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build_index.py
```

Set your hosted API key in the shell:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Do not commit real API keys or paste them into screenshots.

## Quick Start

Ask one question:

```bash
python scripts/query.py "Revenue increased but 7-day retention dropped. Should we launch?" --show-metadata
```

Analyze a synthetic CSV:

```bash
python scripts/analyze_csv.py data/synthetic/guardrail_failure.csv --show-tools
```

Run the FastAPI app:

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## LLM Configuration

Primary hosted model defaults:

```text
EVALRAG_GENERATOR=openai_compatible
EVALRAG_LLM_BASE_URL=https://api.openai.com/v1
EVALRAG_LLM_MODEL=gpt-5.4-mini
EVALRAG_LLM_TOKEN_PARAMETER=max_completion_tokens
```

Fallback local model defaults:

```text
EVALRAG_FALLBACK_LLM_BASE_URL=http://localhost:11434/v1
EVALRAG_FALLBACK_LLM_MODEL=qwen3:8b
EVALRAG_FALLBACK_LLM_TOKEN_PARAMETER=max_tokens
```

If the hosted call fails and Ollama is running with `qwen3:8b`, EvalRAG records:

```text
generator_backend: local_llm_fallback
model: qwen3:8b
generator_error: <primary hosted model error>
```

See `docs/HOSTED_OPENAI_API.md`, `docs/LOCAL_LLM.md`, and `docs/DECISION_EVALUATION.md` for more details.

## Evaluation

The scenario dataset lives at:

```text
data/eval/eval_questions.jsonl
```

Each scenario can specify:

- `expected_sources`: playbook files the retriever should find
- `expected_concepts`: concepts that should appear in the answer
- `expected_decision`: expected launch recommendation label

Run full LLM evaluation:

```bash
python scripts/run_eval.py --save-records logs/openai_eval_full.json
```

Run a small paid sample first:

```bash
python scripts/run_eval.py --limit 5 --save-records logs/openai_eval_sample5.json
```

Run retrieval-only evaluation without calling an LLM:

```bash
python scripts/run_eval.py --retrieval-only
```

Compare retrieval settings without LLM cost:

```bash
python scripts/compare_retrievers.py
```

Current retrieval metrics include:

- `source_hit_at_k`: at least one expected source appeared in top-k
- `source_match_rate`: fraction of expected sources retrieved
- `all_expected_sources_found_rate`: whether all expected sources were found
- `top1_source_match_rate`: whether the top source was expected
- `source_precision_at_k`: fraction of retrieved sources that were expected
- `mean_reciprocal_rank`: how early the first expected source appeared

Answer metrics include:

- `concept_coverage`
- `llm_decision_accuracy`
- `policy_decision_accuracy_when_triggered`
- `final_decision_accuracy`
- `policy_correction_rate`
- `policy_regression_rate`
- `avg_latency_seconds`

## Example Output Shape

```markdown
## Short Answer

## Decision Recommendation
`investigate_further`

## Reasoning

## Metrics to Check

## Suggested Next Steps

## Risks / Caveats

## Policy Validation
Optional section when a hard policy confirms or overrides the LLM proposal.

## Retrieved Sources
```

## Current Limitations

- The playbook is still being expanded and refined.
- Concept coverage currently uses simple text matching, so semantically correct paraphrases may be undercounted.
- The policy validator is conservative and deterministic; future work should move hard constraints into a more structured policy layer.
- The statistical tools are lightweight approximations intended for synthetic demo data, not production experimentation infrastructure.
- Retrieval uses a dependency-light hashed-vector method, not a production embedding database or reranker.

## Recommended Next Steps

1. Expand the product experimentation playbook with reliable public sources and original summaries.
2. Rebuild the index after playbook edits with `python scripts/build_index.py`.
3. Run retrieval-only eval to diagnose source coverage before spending LLM tokens.
4. Run LLM eval and inspect saved records for decision and grounding failures.
5. Expand targeted eval cases for each policy validator rule and inspect `policy_correction_rate` / `policy_regression_rate`.
6. Add stronger faithfulness evaluation, such as LLM-as-judge or a Ragas/DeepEval-style groundedness check.

## Project Identity

This project is not a simple chatbot over markdown files. It is an evaluation-driven RAG prototype for product experimentation analytics, designed to make AI-assisted launch recommendations grounded, inspectable, measurable, and iteratively improvable.
