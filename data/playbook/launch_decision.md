# Launch Decision Framework

## Decision Types

Use a small set of decision labels so launch recommendations stay consistent:

- `launch`: ship broadly after final monitoring checks.
- `partial_rollout`: ship only to safe segments or a small traffic share while monitoring.
- `investigate_further`: do not fully launch until a metric, validity, or business-risk question is resolved.
- `do_not_trust_result`: stop interpreting metric lift until experiment validity is repaired.
- `do_not_launch`: reject or redesign because expected harm outweighs benefit.
- `use_did_or_quasi_experiment`: use a non-randomized causal design instead of a simple A/B readout.

## Full Launch

A full launch is appropriate when the primary metric improves by a practically meaningful amount, the uncertainty is acceptable, sample ratio checks pass, guardrails are stable, and no important segment is harmed. The team should still define post-launch monitors and rollback thresholds.

## Partial Rollout

Partial rollout is appropriate when the treatment appears promising but the evidence is not clean enough for broad exposure. Common reasons include uncertain long-term effects, benefits concentrated in one segment, minor guardrail concerns, or operational risk that can be monitored at low traffic.

## Investigate Further

Investigate further when primary metrics and guardrails disagree, when confidence intervals include meaningful downside, when segment analysis shows possible hidden harm, or when novelty effects may explain a short-term improvement.

## Do Not Trust Result

If sample ratio mismatch, logging failure, assignment bugs, or serious data-quality problems occur, do not use the measured lift as launch evidence. The right decision is to debug the experiment system, repair the data pipeline, or re-run the test.

## Decision Memo Standard

A launch memo should state the recommendation, the primary metric result, guardrail movement, uncertainty, segment findings, validity checks, risks, and next steps. The memo should separate computed facts from policy interpretation.

