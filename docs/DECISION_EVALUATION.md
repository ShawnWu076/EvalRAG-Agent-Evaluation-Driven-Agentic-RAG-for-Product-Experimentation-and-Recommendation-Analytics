# Decision Evaluation and Policy Validation

EvalRAG now records three decision layers for generated answers:

```text
llm_decision -> policy_decision -> final_decision
```

This makes the project more useful for error analysis than a single opaque launch label.

## Decision Layers

### 1. LLM Decision

The OpenAI-compatible LLM reads the user question, retrieved playbook chunks, and optional tool outputs. It writes a memo and chooses one allowed decision label:

- `launch`
- `do_not_launch`
- `investigate_further`
- `partial_rollout`
- `do_not_trust_result`
- `use_did_or_quasi_experiment`

The pipeline parses this from the `## Decision Recommendation` section and stores it as:

```json
"llm_decision": "investigate_further"
```

### 2. Policy Decision

A deterministic policy validator checks high-confidence experimentation constraints. It does not write the memo and does not replace retrieval. It only checks whether the LLM proposal violates known hard policies.

Current policy checks include:

- SRM, assignment, eligibility, or logging validity problems -> `do_not_trust_result`
- Non-random rollout, one-city rollout, pre/post setup -> `use_did_or_quasi_experiment`
- Critical guardrail regression, such as retention or complaint harm -> `investigate_further`
- Important segment harm, such as high-value or Android/Germany harm -> `partial_rollout`
- CTR or click gains with conversion quality loss -> `investigate_further`
- Unsupported fixed guardrail thresholds -> `investigate_further`
- Missing primary metric or guardrails -> `investigate_further`

If a policy triggers, the record stores:

```json
"policy_decision": "investigate_further",
"policy_validation": {
  "policy_action": "override",
  "policy_triggered": true,
  "policy_override": true,
  "policy_findings": [
    {
      "policy_id": "critical_guardrail_regression_blocks_full_launch",
      "recommended_decision": "investigate_further",
      "reason": "...",
      "evidence": "question_text"
    }
  ]
}
```

### 3. Final Decision

The final decision is what the public response and evaluation use as the system recommendation:

```json
"final_decision": "investigate_further",
"decision": "investigate_further"
```

If the LLM decision and policy decision agree, the policy action is `confirm`. If the policy changes the LLM decision, the policy action is `override`. If no hard policy applies, the final decision stays equal to the LLM decision.

## Why This Matters

This lets us answer better debugging questions:

```text
Did the LLM decide correctly?
Did the policy validator catch unsafe launch recommendations?
Did the final system decision match the expected label?
If the system failed, was it retrieval, playbook coverage, LLM reasoning, or policy overreach?
```

That is the heart of evaluation-driven RAG.

## Running Evaluation

Run a small LLM eval and save records:

```bash
python scripts/run_eval.py --limit 5 --save-records logs/openai_eval_sample5.json
```

Inspect decision layers:

```bash
python - <<'PY'
import json
records = json.load(open("logs/openai_eval_sample5.json"))
for r in records:
    print(
        r["eval_id"],
        "llm=", r.get("llm_decision"),
        "policy=", r.get("policy_decision"),
        "final=", r.get("final_decision"),
        "expected=", r.get("expected_decision"),
        "action=", r.get("policy_validation", {}).get("policy_action"),
    )
PY
```

Run retrieval-only eval when you do not want to spend LLM tokens:

```bash
python scripts/run_eval.py --retrieval-only
```

## Metrics Added

`run_eval.py` now reports:

- `llm_decision_accuracy`: whether the LLM proposal matched the expected label
- `policy_decision_accuracy_when_triggered`: whether triggered policy decisions matched expected labels
- `final_decision_accuracy`: whether the final hybrid decision matched expected labels
- `policy_trigger_rate`: how often the validator found a relevant policy
- `policy_override_rate`: how often policy changed the LLM decision
- `policy_correction_rate`: how often policy fixed an incorrect LLM decision
- `policy_regression_rate`: how often policy changed a correct LLM decision into an incorrect final decision

The saved failure records also include `failure_hypothesis`, with rough categories such as:

- `retrieval_or_playbook_gap`
- `llm_reasoning_or_prompt_gap`
- `retrieval_then_llm_decision_gap`
- `policy_validator_overreach`
- `answer_concept_coverage_gap`

## Current Limitation

The policy validator is intentionally conservative and deterministic. It is not a replacement for a full product policy engine. The next mature step is to move more of these hard constraints into a structured policy/playbook format and test each policy rule against targeted eval scenarios.
