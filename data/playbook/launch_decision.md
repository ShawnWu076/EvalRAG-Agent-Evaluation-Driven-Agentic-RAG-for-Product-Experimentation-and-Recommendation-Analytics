# Launch Decision Framework

This playbook defines how the agent should translate experiment evidence, metric tradeoffs, product risk, and business context into a launch recommendation.

This file is designed for an evaluation-driven Agentic RAG system. The goal is not only to help the agent answer product experimentation questions, but also to make the answer auditable.

A good answer should make clear:

- what decision is being made;
- what evidence supports the decision;
- what evidence is missing;
- whether the experiment result can be trusted;
- which metrics matter most;
- which guardrails limit the decision;
- what uncertainty remains;
- and what the next responsible action should be.

The agent should not mechanically recommend launch because one metric improved. It should also not mechanically block every launch because one secondary metric moved slightly negative.

The correct launch decision is **risk-aware, evidence-based, and reversible when uncertainty is high**.

---

## Quick Retrieval Summary

Use this playbook when the user asks whether to launch, stop, roll out, restrict, or further investigate a product change.

This playbook is especially relevant when:

- one metric improves while another metric worsens;
- the user asks whether an experiment result is good enough to ship;
- short-term engagement conflicts with retention, monetization, trust, safety, or ecosystem quality;
- the result may be statistically significant but not practically meaningful;
- the experiment may have SRM, telemetry, randomization, logging, or attribution issues;
- effects differ across user, creator, seller, advertiser, geography, platform, or content segments;
- the user asks a vague product strategy question such as “how should we think about this?”;
- the evidence is observational rather than randomized.

Default reasoning order:

1. Clarify the decision.
2. Validate experiment trustworthiness.
3. Classify risk tier and reversibility.
4. Define metric hierarchy.
5. Evaluate practical significance and uncertainty.
6. Check guardrails.
7. Analyze segment heterogeneity.
8. Consider long-term, marketplace, and ecosystem risk.
9. Choose one allowed decision label.
10. State missing evidence and next steps.

---

## 1. Core Principle

A launch decision should maximize durable product value while controlling downside risk.

The agent should reason from evidence, not vibes.

A good launch decision depends on:

- whether the experiment result is trustworthy;
- whether the decision metric improved by a practically meaningful amount;
- whether the metric is aligned with durable user or business value;
- whether guardrail deterioration is within acceptable tolerance;
- whether important user, creator, seller, advertiser, or marketplace segments are harmed;
- whether the decision is reversible;
- whether the feature creates long-term, marketplace, trust/safety, policy, or ecosystem risk;
- whether the cost of being wrong is low or high.

When evidence is incomplete, the agent should make uncertainty explicit and recommend the smallest responsible next step.

The agent should avoid both extremes:

- over-launching because one metric improved;
- over-blocking because one minor secondary metric moved slightly negative.

---

## 2. Decision Labels

The agent should use exactly one primary decision label.

Allowed labels:

- `launch`
- `launch_with_monitoring`
- `partial_rollout`
- `investigate_further`
- `do_not_trust_result`
- `do_not_launch`
- `use_did_or_quasi_experiment`

The agent may mention a secondary action, but the final answer should still contain one primary decision label.

---

## 3. Label Boundary Rules

Use exactly one primary decision label.

Important boundaries:

- `launch` means broad release is justified.
- `launch_with_monitoring` means broad release is acceptable, but explicit monitoring and rollback thresholds are required.
- `partial_rollout` means broad release is not yet justified, but limited controlled exposure is justified.
- `investigate_further` means more analysis, measurement, diagnosis, or rerun is needed before increasing exposure.
- `do_not_trust_result` means the experiment result should not be interpreted as causal evidence.
- `do_not_launch` means the expected harm or downside risk outweighs the expected benefit.
- `use_did_or_quasi_experiment` means the question is causal, but clean randomized evidence is unavailable or inappropriate.

Do not use `partial_rollout` as a vague compromise. Use it only when the agent can specify:

- target segment;
- rollout size;
- rollout duration;
- monitoring metrics;
- rollback thresholds;
- expansion criteria.

Do not use `launch_with_monitoring` if a key guardrail already exceeds the acceptable harm threshold.

Do not use `launch` only because a metric is statistically significant.

Do not use `investigate_further` as a generic answer. Specify exactly what evidence is missing and how it would change the decision.

---

## 4. Detailed Decision Labels

### 4.1 `launch`

Use `launch` when the evidence is strong enough for broad release.

A full launch is appropriate when:

- experiment validity checks pass;
- the decision metric improves by a practically meaningful amount;
- the effect is aligned with the product goal;
- key guardrails are stable or within acceptable deterioration tolerance;
- no strategically important segment is harmed;
- long-term risk is low or well-monitored;
- the feature is operationally ready;
- rollback plans and monitoring are defined.

Do not recommend full launch only because one metric is statistically significant.

Bad reasoning:

> Conversion increased with p < 0.05, so we should launch.

Better reasoning:

> Conversion increased by a practically meaningful amount, the confidence interval excludes material downside, SRM and logging checks passed, revenue and retention guardrails are stable, no key segment is harmed, and the change is reversible. Recommend launch with standard post-launch monitoring.

---

### 4.2 `launch_with_monitoring`

Use `launch_with_monitoring` when broad launch is reasonable, but there are still risks that require explicit post-launch tracking.

This is appropriate when:

- evidence is mostly positive;
- guardrail movement is slightly negative but within pre-defined tolerance;
- long-term risk exists but is not severe;
- the decision is reversible;
- there is a clear rollback threshold;
- the team can monitor the feature after launch.

The agent should specify:

- what to monitor;
- for how long;
- what threshold would trigger rollback;
- which segments require extra attention.

Example:

> Launch with monitoring. The activation lift is meaningful and validity checks pass, but existing-user retention is slightly negative. Because the decline is within tolerance and the feature is reversible, ship with a 14-day retention monitor and rollback if existing-user retention drops more than 0.3 percentage points.

---

### 4.3 `partial_rollout`

Use `partial_rollout` when the treatment is promising but not safe or certain enough for broad launch.

A partial rollout is appropriate when:

- the treatment works for a specific segment but not broadly;
- uncertainty remains;
- guardrail degradation is small but worth monitoring;
- long-term effects are unclear;
- novelty effects may be present;
- operational risk should be tested at low traffic;
- ecosystem or marketplace impact is possible;
- the upside is meaningful, but the cost of a full false-positive launch is high.

A partial rollout recommendation should specify:

- target segment;
- traffic percentage;
- rollout duration;
- metrics to monitor;
- rollback thresholds;
- decision criteria for expanding or stopping the rollout.

Bad reasoning:

> This looks promising, so let’s partially roll it out.

Better reasoning:

> Partial rollout to new users only. The activation lift is concentrated among new users, while existing-user retention is slightly negative. Roll out to 10% of eligible new users for two weeks, monitor 7-day retention, complaint rate, latency, and revenue per user, and expand only if existing-user guardrails remain within tolerance.

---

### 4.4 `investigate_further`

Use `investigate_further` when evidence is directionally interesting but insufficient for a responsible launch decision.

This applies when:

- primary metric and guardrails disagree;
- confidence intervals include meaningful downside;
- the experiment may be underpowered;
- segment analysis shows conflicting effects;
- novelty, seasonality, or external events may explain the result;
- metric definitions are unclear;
- the user’s question is ambiguous;
- important business context is missing;
- long-term risk may be material.

The agent should not vaguely say “we need more data.” It should specify exactly what data or analysis is missing.

Bad:

> We need more data.

Better:

> Investigate further. We need the 7-day and 28-day retention readout, SRM diagnosis, revenue per user by segment, report/hide rate, and a breakdown by new versus existing users before deciding whether the engagement lift is safe to launch.

---

### 4.5 `do_not_trust_result`

Use `do_not_trust_result` when the experiment result should not be interpreted as valid evidence.

This applies when there are serious trust or data quality issues, such as:

- sample ratio mismatch;
- randomization failure;
- assignment imbalance;
- unstable assignment;
- treatment/control contamination;
- missing telemetry;
- duplicated events;
- inconsistent logging between variants;
- exposure definition mismatch;
- post-treatment filtering;
- bot or spam imbalance;
- pipeline changes during the experiment;
- metric instrumentation changes during the experiment.

When using this label, the agent should not discuss the measured lift as if it were causal evidence.

Bad:

> Conversion increased by 3%, but there is SRM, so maybe launch carefully.

Better:

> Do not trust the result. SRM means the treatment and control groups may not be comparable. The measured 3% lift should not be used as launch evidence until the SRM root cause is diagnosed and the experiment is repaired or rerun.

---

### 4.6 `do_not_launch`

Use `do_not_launch` when the expected harm outweighs the expected benefit.

This applies when:

- the decision metric declines meaningfully;
- guardrail deterioration exceeds acceptable tolerance;
- the feature improves a shallow short-term metric while damaging long-term product value;
- the benefit is concentrated in low-value or harmful behavior;
- the feature creates trust, safety, policy, regulatory, privacy, fairness, brand, or ecosystem risk;
- an important segment is harmed;
- maintenance cost or operational complexity exceeds expected benefit;
- the feature encourages behavior the platform does not want to amplify.

Do not launch merely because “harm is not statistically significant.” Lack of statistically significant harm is not the same as evidence of safety, especially when downside risk is high.

---

### 4.7 `use_did_or_quasi_experiment`

Use this label when the question is causal, but the available evidence does not come from a clean randomized experiment.

This applies when:

- randomization is impossible, unethical, or unavailable;
- the treatment was rolled out by geography, time, policy status, eligibility rule, creator group, seller group, or platform;
- exposure is endogenous;
- the data is observational;
- there are marketplace, network, or interference effects;
- the user is asking about policy impact or strategic causal impact.

Possible methods:

- Difference-in-Differences;
- synthetic control;
- regression discontinuity;
- instrumental variables;
- matching or weighting;
- interrupted time series;
- geo experiments;
- switchback experiments.

The agent should state that quasi-experimental methods require stronger assumptions than randomized A/B tests.

---

## 5. Risk Tier and Reversibility

The evidence threshold should depend on the risk level of the decision.

Low-risk, reversible changes can tolerate more uncertainty. High-risk, hard-to-reverse, marketplace-level, ranking-level, ads-level, policy-level, or trust/safety changes require stronger evidence.

Classify the decision into one of four tiers.

---

### 5.1 `low_risk_reversible`

Small UI, copy, layout, or workflow changes with limited downside and easy rollback.

Examples:

- button copy;
- minor UI layout;
- onboarding text;
- tooltip;
- low-impact email copy;
- small visual treatment.

Evidence standard:

- trustworthy experiment;
- meaningful primary metric movement;
- no major guardrail harm;
- basic segment sanity check.

Possible decisions:

- `launch`;
- `launch_with_monitoring`;
- `partial_rollout`.

---

### 5.2 `medium_risk_reversible`

Feature changes that affect user behavior but can be rolled back quickly.

Examples:

- new onboarding flow;
- new recommendation module;
- new checkout element;
- new search filter;
- new notification format;
- new profile feature.

Evidence standard:

- trustworthy experiment;
- practical significance;
- guardrails within tolerance;
- segment analysis for key user groups;
- clear rollback plan.

Possible decisions:

- `launch`;
- `launch_with_monitoring`;
- `partial_rollout`;
- `investigate_further`.

---

### 5.3 `high_risk_reversible`

Changes that affect ranking, recommendations, ads, marketplace dynamics, creator incentives, or user attention at scale.

Examples:

- feed ranking change;
- recommendation model change;
- ads load change;
- marketplace matching change;
- creator distribution change;
- notification volume change;
- pricing display change;
- search ranking change.

Evidence standard:

- trustworthy experiment;
- strong decision metric evidence;
- explicit guardrail tolerance;
- segment analysis;
- ecosystem monitoring;
- rollback threshold;
- longer-term readout if short-term and long-term incentives may diverge.

Possible decisions:

- `partial_rollout`;
- `investigate_further`;
- `launch_with_monitoring`;
- `do_not_launch`;
- `launch` only with strong evidence and monitoring.

---

### 5.4 `high_risk_irreversible`

Changes involving pricing, policy, safety, privacy, compliance, brand trust, or irreversible user harm.

Examples:

- content policy change;
- trust and safety enforcement change;
- privacy-sensitive feature;
- underage user experience;
- pricing model change;
- creator monetization rule;
- account enforcement rule;
- financial eligibility rule.

Evidence standard:

- high confidence;
- explicit downside analysis;
- stakeholder review if relevant;
- legal, policy, or compliance review if relevant;
- long-term monitoring;
- conservative guardrails.

Possible decisions:

- usually `investigate_further`, `partial_rollout`, or `do_not_launch`;
- full launch only when evidence is strong and downside is controlled.

---

## 6. Metric Hierarchy

The agent must classify metrics before making a decision.

Not all metrics have equal decision weight.

---

### 6.1 Overall Evaluation Criterion / Decision Metric

The OEC or decision metric is the metric, or metric bundle, that best represents the product objective.

A good decision metric should:

- align with durable user or business value;
- avoid over-optimizing shallow short-term behavior;
- be sensitive enough for experimentation;
- be interpretable by product, engineering, and data science stakeholders;
- connect short-term measurable outcomes to long-term product goals.

Examples:

For recommendations:

- qualified engagement;
- long-term retention;
- satisfaction;
- successful sessions;
- content diversity;
- return rate.

For ads:

- revenue quality;
- advertiser ROI;
- user retention;
- ad load tolerance;
- conversion quality.

For marketplaces:

- completed transactions;
- buyer retention;
- seller retention;
- liquidity;
- quality-adjusted GMV;
- refund rate.

For onboarding:

- activation;
- qualified first action;
- early retention;
- setup completion.

For trust and safety:

- harmful exposure;
- reports;
- enforcement accuracy;
- appeal rate;
- user trust;
- long-term retention.

---

### 6.2 Success Metrics

Success metrics are expected to improve if the product hypothesis is correct.

Examples:

- activation rate;
- conversion rate;
- 7-day retention;
- revenue per user;
- average order value;
- qualified watch time;
- cross-sell attachment rate;
- successful sessions;
- creator posting rate;
- buyer purchase rate.

Success metrics should be connected to the experiment hypothesis.

Bad:

> The feature increased clicks, so it worked.

Better:

> The feature was designed to improve onboarding activation. Activation increased meaningfully, while clicks are only diagnostic.

---

### 6.3 Guardrail Metrics

Guardrails are metrics the treatment must not materially harm.

Examples:

- latency;
- crash rate;
- error rate;
- churn;
- complaint rate;
- hide/report/block rate;
- refund rate;
- cancellation rate;
- advertiser ROI;
- seller retention;
- creator retention;
- trust/safety violations;
- content quality;
- marketplace liquidity.

Guardrails should protect the product from harmful local optimization.

---

### 6.4 Diagnostic Metrics

Diagnostic metrics explain mechanism but should not usually drive the launch decision alone.

Examples:

- CTR;
- impressions;
- scroll depth;
- number of recommendations shown;
- notification opens;
- short clicks;
- dwell time on a narrow surface;
- session count;
- click depth;
- feed refreshes.

A diagnostic metric lift is not sufficient for launch if the decision metric or guardrails do not support it.

---

## 7. Pre-Specified Shipping Criteria

A good experiment should define shipping criteria before reading the result.

The launch memo should specify:

- what metric must improve;
- how large the improvement must be to matter;
- which guardrails must not deteriorate beyond acceptable tolerance;
- which segments must be protected;
- what validity checks must pass;
- what result pattern leads to `launch`;
- what result pattern leads to `partial_rollout`;
- what result pattern leads to `investigate_further`;
- what result pattern leads to `do_not_trust_result`;
- what result pattern leads to `do_not_launch`.

Avoid changing the decision rule after seeing results.

Bad:

> Retention was flat, but CTR improved, so this is a win.

Better:

> The pre-specified success metric was 7-day retention. CTR was diagnostic. Since retention did not improve and CTR increased, this is not enough for full launch.

For evaluation-driven RAG, the agent should be penalized if it cherry-picks a favorable metric while ignoring the stated decision metric.

---

## 8. Required Reasoning Order

For every launch decision, the agent should reason in this order.

---

### Step 1: Clarify the Decision

Identify what decision the user is asking for.

Examples:

- Should we launch this feature?
- Should we roll it out to all users?
- Should we keep experimenting?
- Should we restrict it to a segment?
- Should we redesign the feature?
- Should we stop encouraging a behavior?
- Should we use a causal design instead of a simple A/B readout?

If the user asks an ambiguous question like “how should we think about this?”, translate it into a decision problem.

---

### Step 2: Identify Product Context and Decision Owner

A launch decision depends on product context.

The agent should infer or ask:

- What is the company or product surface?
- What is the feature, policy, ranking change, or model change?
- Who is affected?
- What is the intended product goal?
- What is the cost of a wrong launch?
- Is the decision reversible?
- Is this a user experience, recommendation, ads, marketplace, policy, trust/safety, or infrastructure decision?

A reversible UI change can tolerate more uncertainty than a pricing, policy, recommendation, safety, or marketplace intervention.

---

### Step 3: Classify Risk Tier

Classify the launch as:

- `low_risk_reversible`;
- `medium_risk_reversible`;
- `high_risk_reversible`;
- `high_risk_irreversible`.

The higher the risk tier, the stronger the evidence requirement.

---

### Step 4: Define the Metric Hierarchy

Identify:

- decision metric / OEC;
- success metrics;
- guardrail metrics;
- diagnostic metrics;
- long-term proxy metrics.

If the metric hierarchy is missing, the agent should not pretend the launch decision is fully determined.

---

### Step 5: Check Experiment Trustworthiness

Before interpreting metric movement, check whether the experiment can be trusted.

Important validity checks:

- sample ratio mismatch;
- correct randomization unit;
- stable assignment;
- no treatment contamination;
- consistent exposure logging;
- metric logging completeness;
- no post-treatment filtering;
- no major data pipeline changes;
- no severe missing data;
- no duplicated users or events;
- no bot or spam imbalance;
- no instrumentation changes during the experiment.

If these checks fail seriously, use `do_not_trust_result`.

The agent should not treat invalid experimental results as causal evidence.

---

### Step 6: Check Practical Significance

Statistical significance is not enough.

The agent should ask:

- Is the lift large enough to matter?
- Does the effect justify engineering and maintenance cost?
- Does the effect matter at business scale?
- Is the effect meaningful relative to historical variance?
- Would the decision change if the true effect were near the lower bound of the confidence interval?
- Does the effect improve durable value or only a shallow proxy?

A tiny statistically significant lift may not justify launch if the feature adds complexity, degrades user experience, or creates long-term risk.

---

### Step 7: Check Uncertainty

The agent should consider:

- confidence interval;
- p-value or posterior uncertainty;
- sample size;
- power;
- experiment duration;
- multiple testing;
- peeking or early stopping;
- novelty effects;
- seasonality;
- heterogeneous treatment effects.

If uncertainty is high, prefer `partial_rollout` or `investigate_further` over full launch.

---

### Step 8: Evaluate Guardrails

Guardrails protect the product, business, users, and ecosystem from harmful launches.

The agent should check:

- user experience guardrails;
- business guardrails;
- trust and safety guardrails;
- marketplace guardrails;
- infrastructure guardrails;
- fairness or segment guardrails.

A feature should not be launched broadly if it improves the success metric by exploiting or damaging an important guardrail.

---

### Step 9: Analyze Segments

Averages can hide harm.

The agent should check whether treatment effects differ across:

- new vs existing users;
- high-value vs low-value users;
- power users vs casual users;
- paid vs free users;
- creators vs consumers;
- buyers vs sellers;
- advertisers vs users;
- geographies;
- platforms;
- acquisition channels;
- content categories;
- user intent groups;
- risk or safety groups.

A launch may be appropriate for one segment and harmful for another.

Use `partial_rollout` when the benefit is segment-specific and broad launch would expose harmed segments.

---

### Step 10: Evaluate Long-Term and Ecosystem Risk

Short experiments may miss long-term harm.

The agent should watch for:

- novelty effects;
- user fatigue;
- shallow engagement;
- content quality degradation;
- creator or seller incentive shifts;
- marketplace imbalance;
- ad saturation;
- cannibalization of existing surfaces;
- trust and safety externalities;
- brand risk;
- regulatory or policy risk.

If long-term risk is material, prefer:

- longer experiment duration;
- holdout groups;
- phased rollout;
- post-launch monitoring;
- rollback thresholds;
- ecosystem-level metrics.

---

### Step 11: Make Decision and State Missing Evidence

The final answer should include:

- decision label;
- reasoning summary;
- key supporting evidence;
- key risks;
- missing evidence;
- next steps.

The agent should avoid overconfident recommendations when important evidence is missing.

---

## 9. Handling Missing or Ambiguous Information

Users often do not provide a complete experiment readout.

If key information is missing, the agent should still provide a provisional recommendation, but must label it as conditional.

Do not ask a long list of clarifying questions before giving value. Instead:

1. restate the likely decision problem;
2. give a provisional decision label if possible;
3. list the 3–5 most decision-critical missing inputs;
4. explain how the recommendation would change under different outcomes.

Example:

> Provisional decision: investigate_further. Based on the information provided, the feature has a possible engagement benefit, but we do not yet know whether the lift is trustworthy, whether retention or revenue guardrails are harmed, or whether the effect is concentrated in a risky segment. If SRM passes and guardrails are stable, partial rollout may be reasonable. If trust/safety or retention deteriorates materially, do not launch.

The agent should avoid pretending the decision is fully determined when essential evidence is missing.

---

## 10. Guardrail Framework

Guardrails determine whether a product change is safe to ship.

There are two major types of guardrails:

1. trust-related guardrails;
2. organizational guardrails.

---

### 10.1 Trust-Related Guardrails

Trust-related guardrails determine whether the experiment result can be interpreted.

Examples:

- sample ratio mismatch;
- assignment imbalance;
- missing telemetry;
- duplicated events;
- inconsistent treatment/control logging;
- biased triggered analysis;
- post-treatment filtering;
- bot or spam imbalance;
- data pipeline changes during the experiment;
- metric instrumentation changes during the experiment.

If trust-related guardrails fail, use `do_not_trust_result`.

Do not use a broken experiment as causal evidence.

---

### 10.2 Organizational Guardrails

Organizational guardrails determine whether the product change is safe for the business, users, and ecosystem.

Examples:

- retention;
- revenue;
- latency;
- crash rate;
- refunds;
- complaints;
- trust/safety violations;
- advertiser ROI;
- creator or seller health;
- marketplace liquidity;
- content quality;
- support tickets;
- user trust.

If organizational guardrails fail, the experiment may still be statistically valid, but the product decision may be `partial_rollout`, `investigate_further`, or `do_not_launch`.

---

### 10.3 Guardrail Tolerance and Non-Inferiority Logic

A guardrail does not always need to improve. Often it needs to not deteriorate beyond an acceptable threshold.

For guardrails, the question is not always:

> Did this metric move at all?

The better question is:

> Did this metric get worse by more than the maximum acceptable harm?

Examples:

- latency must not increase by more than 20 ms;
- crash rate must not increase by more than 0.1 percentage points;
- refund rate must not increase by more than 0.2 percentage points;
- 7-day retention must not decrease by more than 0.3 percentage points;
- advertiser ROI must not decrease beyond agreed tolerance;
- seller retention must not decline beyond agreed tolerance.

If guardrail deterioration is small and within pre-defined tolerance, the agent may recommend `launch_with_monitoring` or `partial_rollout`, depending on risk tier.

If guardrail deterioration exceeds tolerance, prefer `do_not_launch` or `investigate_further`.

For high-risk irreversible decisions, tolerance should be stricter.

---

## 11. Metric Tradeoff Framework

Many real product decisions involve metric tradeoffs.

The agent should not assume all metric increases are good.

---

### 11.1 Classify the Metrics

For each metric, classify it as:

- decision metric;
- success metric;
- guardrail metric;
- diagnostic metric;
- long-term proxy metric;
- business outcome metric;
- trust/safety metric.

Example:

- Watch time: engagement metric.
- Retention: durable user value metric.
- Revenue per user: monetization metric.
- Reports or hides: user dissatisfaction metric.
- Low-quality content exposure: platform health guardrail.
- CTR: often diagnostic, not sufficient by itself.

---

### 11.2 Determine Whether Metrics Are Substitutes or Complements

Some metrics move together. Others trade off.

Examples:

- More recommendations may increase watch time but reduce satisfaction.
- More ads may increase short-term revenue but reduce retention.
- More discounts may increase conversion but reduce margin.
- More controversial content may increase engagement but damage trust and advertiser value.
- More notifications may increase sessions but increase opt-outs or churn.

If the tradeoff is between short-term engagement and long-term platform health, the agent should be conservative.

---

### 11.3 Identify the Strategic Metric

The strategic metric is the metric the company should ultimately optimize for.

Examples:

- A marketplace should not optimize only for buyer clicks if seller quality collapses.
- A recommendation system should not optimize only for watch time if it increases harmful content.
- An ads system should not optimize only for ad revenue if advertiser ROI declines.
- A social platform should not optimize only for engagement if user trust and content quality decline.
- An onboarding flow should not optimize only for signups if activated users do not retain.

When short-term and long-term metrics conflict, prefer the metric closer to durable product value.

---

## 12. Segment Analysis Framework

Averages can hide harm.

The agent should check whether treatment effects differ across:

- new vs existing users;
- high-value vs low-value users;
- power users vs casual users;
- paid vs free users;
- creators vs consumers;
- buyers vs sellers;
- advertisers vs users;
- geographies;
- platforms;
- acquisition channels;
- content categories;
- user intent groups;
- safety-sensitive groups;
- risk groups.

A launch may be appropriate for one segment and harmful for another.

Use `partial_rollout` when:

- the feature clearly benefits one segment;
- the harmed segment is strategically important;
- the average effect is positive but distribution is uneven;
- the feature should be restricted until more evidence is collected.

Example:

> If a feature improves new-user activation but hurts long-term power-user retention, full launch is risky. A better decision may be targeted rollout for new users while monitoring long-term retention and satisfaction.

The agent should avoid saying “average treatment effect is positive, so launch” without checking segment heterogeneity.

The agent should also avoid overreacting to noisy segment results. Segment findings should be interpreted with attention to:

- sample size;
- multiple testing;
- whether segments were pre-specified;
- whether the segment is strategically important;
- whether the effect is large enough to matter.

---

## 13. Long-Term Risk Framework

Some launches look good in short-term experiments but are bad long-term product decisions.

The agent should watch for:

- novelty effects;
- habit formation vs shallow engagement;
- user fatigue;
- creator or seller incentives;
- content quality degradation;
- ad saturation;
- marketplace imbalance;
- cannibalization of existing surfaces;
- trust and safety externalities;
- brand or regulatory risk.

A short experiment may not capture:

- long-term retention;
- lifetime value;
- ecosystem quality;
- creator behavior;
- advertiser trust;
- user perception;
- policy risk.

When long-term risk is material, prefer:

- longer experiment duration;
- long-term holdout groups;
- phased rollout;
- post-launch rollback thresholds;
- long-term guardrail monitoring.

---

## 14. Interference and Marketplace Effects

Some experiments violate the assumption that one unit's treatment does not affect another unit's outcome.

Watch for interference when the product involves:

- social graphs;
- feeds;
- recommendation systems;
- ads auctions;
- marketplaces;
- creator ecosystems;
- inventory allocation;
- ranking systems;
- network effects.

Examples:

- A ranking change may shift traffic from one creator group to another.
- An ads change may improve short-term revenue but reduce advertiser ROI.
- A marketplace change may improve buyer conversion while hurting seller retention.
- A recommendation model may increase engagement for treated users while degrading content diversity or creator incentives.
- A feed change may affect untreated users through friend or creator behavior.

If interference is likely, the agent should be cautious about user-level A/B interpretation and may recommend:

- cluster randomization;
- geo experiments;
- switchback experiments;
- marketplace-level holdouts;
- longer-term ecosystem monitoring;
- quasi-experimental analysis.

Use `use_did_or_quasi_experiment` when randomized evidence is unavailable or inappropriate.

---

## 15. Peeking and Sequential Decisions

If the team repeatedly checks results before the planned end date, standard p-values may become misleading.

The agent should ask:

- Was the experiment duration pre-specified?
- Was early stopping allowed?
- Was a sequential testing method used?
- Were results monitored for safety only, or used for launch decisions?
- Did the team stop the test because the result looked favorable?
- Was the final readout based on a fixed horizon or an anytime-valid method?

Monitoring guardrails for safety is acceptable.

Using repeated unplanned checks to declare success is not.

If no sequential method was used, be cautious about launch decisions based on early favorable results.

---

## 16. Decision Matrix

Use this matrix to convert evidence into a recommendation.

| Evidence Pattern | Recommended Decision |
|---|---|
| Decision metric meaningfully improves, guardrails stable, validity checks pass, no important segment harmed, risk is low or controlled | `launch` |
| Decision metric improves, guardrails are within tolerance, but some uncertainty remains | `launch_with_monitoring` or `partial_rollout` |
| Decision metric improves, but long-term risk or segment risk is unclear | `partial_rollout` or `investigate_further` |
| Success metric improves, but key guardrail exceeds acceptable harm threshold | `do_not_launch` or `investigate_further` |
| Average effect is positive, but a key segment is harmed | `partial_rollout` or `investigate_further` |
| Result has SRM, logging failure, assignment bug, or severe data quality issue | `do_not_trust_result` |
| Short-term engagement improves but monetization, safety, trust, or ecosystem quality declines materially | usually `do_not_launch` or `partial_rollout` with strict guardrails |
| No statistically significant harm, but experiment is underpowered and downside risk is high | `investigate_further` |
| Observational result is being interpreted causally | `use_did_or_quasi_experiment` |
| Benefit is too small to justify cost or complexity | `do_not_launch` or `investigate_further` |
| Strong benefit concentrated in a safe, valuable segment | `partial_rollout` |
| Low-risk reversible change, small positive lift, guardrails stable | `launch_with_monitoring` may be acceptable |
| High-risk irreversible change, moderate positive lift, long-term risk unclear | `investigate_further` or `partial_rollout` |
| Diagnostic metric improves but decision metric is flat or negative | usually `investigate_further` or `do_not_launch` |
| Primary result is favorable but repeated unplanned peeking occurred | `investigate_further` unless sequential testing was used |

---

## 17. Ambiguous Product Question Handling

Users may ask vague questions such as:

- “How should we think about this?”
- “Is this good or bad?”
- “Should we encourage this behavior?”
- “Retention went up but revenue went down. What should we do?”
- “This content type increases engagement but attracts low-value users. Is that okay?”
- “CTR improved but satisfaction declined. Should we ship?”

For ambiguous questions, the agent should structure the answer as:

1. Restate the decision problem.
2. Identify the core tradeoff.
3. Define the likely decision metric.
4. Identify success metrics and guardrails.
5. Explain what evidence supports launch.
6. Explain what evidence blocks launch.
7. Recommend a decision label.
8. List missing evidence.
9. Propose next analysis or experiment.

The agent should not answer vague product questions with generic advice. It should convert ambiguity into a structured product decision.

---

## 18. Example: Engagement Up, Monetization Down

### User Question

> We found that borderline content increases retention and time spent, but users who consume this content monetize poorly. How should we think about this?

### Good Agent Reasoning

This is not simply an engagement win. It is a tradeoff between short-term engagement, monetization quality, user intent, platform health, and trust/safety risk.

The agent should ask:

- Is the content policy-compliant?
- Does it increase long-term retention or only short-term time spent?
- Does it reduce ad quality, advertiser trust, or conversion?
- Are these users incremental, or are they displacing healthier users?
- Does this content increase reports, hides, complaints, or churn among other users?
- Does it change creator incentives toward lower-quality content?
- Is the monetization weakness caused by user demographics, ad suitability, content adjacency, or low purchase intent?
- Is the evidence randomized or observational?
- Are there spillover effects on the broader content ecosystem?

Possible recommendation:

- If the content creates safety, trust, advertiser-quality, or ecosystem risk, do not optimize for it even if engagement rises.
- If the content is policy-compliant and only works for a narrow low-risk segment, consider limited ranking exposure with strict guardrails.
- If the result is observational, use a randomized ranking experiment or quasi-experimental design before making a causal claim.

Likely decision:

- `investigate_further` if evidence is incomplete.
- `do_not_launch` if safety, trust, advertiser, or ecosystem risk is material.
- `partial_rollout` only if the behavior is safe, measurable, reversible, and limited to a clearly beneficial segment.

### Bad Answer Pattern

> Retention and time spent increased, so we should promote this content.

This is bad because it ignores monetization quality, trust/safety, advertiser value, and ecosystem incentives.

---

## 19. Example: New Feature Helps New Users but Hurts Existing Users

### User Question

> A new feature improves activation for new users but slightly lowers retention for existing users. Should we launch?

### Good Agent Reasoning

This is a segment-level tradeoff. The average effect is not enough.

The agent should ask:

- Are new users the intended target?
- How large is the activation lift?
- How large is the existing-user retention decline?
- Are existing users high-value or strategically important?
- Can the feature be targeted only to new users?
- Is the retention decline temporary novelty friction or persistent harm?
- Are there guardrail impacts on revenue, satisfaction, latency, or support tickets?
- Is the decline within pre-defined tolerance?

Possible recommendation:

- Full launch is risky if existing users are harmed.
- A targeted rollout to new users may be appropriate if the activation lift is meaningful and existing-user harm can be avoided.
- Continue monitoring long-term retention for cohorts exposed to the feature.

Likely decision:

- `partial_rollout`.

---

## 20. Example: Metric Lift but SRM Detected

### User Question

> Treatment increased conversion by 3%, but the sample ratio is off. Should we launch?

### Good Agent Reasoning

Do not use the measured lift as launch evidence until the SRM is diagnosed.

The agent should check:

- Was randomization implemented correctly?
- Were users dropped after assignment?
- Did logging differ by treatment group?
- Did one variant fail to load?
- Was there bot, geography, platform, or eligibility imbalance?
- Was analysis performed on the assigned population or only exposed users?

Likely decision:

- `do_not_trust_result`.

The next step is to diagnose the SRM, repair the pipeline or assignment issue, and rerun or reanalyze the experiment.

### Bad Answer Pattern

> The lift is positive, but SRM is a concern. Maybe launch cautiously.

This is bad because SRM can invalidate the comparison. The lift should not be treated as causal launch evidence.

---

## 21. Example: Recommendation System Improves CTR but Hurts Long-Term Retention

### User Question

> A recommendation model improves CTR but slightly hurts 7-day retention. Should we ship it?

### Good Agent Reasoning

CTR is often a short-term diagnostic metric. Retention is closer to durable user value.

The agent should ask:

- Is CTR the decision metric or only diagnostic?
- Does the model increase low-quality clicks?
- Does it create clickbait or shallow engagement?
- What happens to watch time, satisfaction, hides, reports, and return rate?
- Is the retention decline statistically and practically meaningful?
- Does the effect differ by new vs existing users?
- Is the model changing creator incentives or content diversity?

Possible recommendation:

- Do not fully launch if the retention decline is meaningful.
- Consider partial rollout only if the CTR lift is strategically important and retention harm is small, uncertain, or concentrated in a non-core segment.
- Investigate ranking quality and long-term satisfaction before launch.

Likely decision:

- `investigate_further` or `do_not_launch`.

---

## 22. Example: Ads Revenue Up but Advertiser ROI Down

### User Question

> A new ads ranking model increases short-term ad revenue by 5%, but advertiser ROI drops. Should we launch?

### Good Agent Reasoning

This is a monetization-quality tradeoff. Short-term platform revenue may be coming from lower advertiser efficiency.

The agent should ask:

- Is the revenue lift incremental or caused by higher ad load?
- Does advertiser ROI decline beyond tolerance?
- Are conversions lower quality?
- Are advertisers likely to reduce future spend?
- Does user retention or ad fatigue worsen?
- Is the effect concentrated in certain advertiser segments?
- Does the model harm marketplace trust between advertisers and the platform?

Possible recommendation:

- Do not fully launch if advertiser ROI deterioration is material.
- Consider partial rollout only if ROI decline is within tolerance and long-term advertiser retention is monitored.
- Investigate auction quality, conversion quality, and advertiser retention.

Likely decision:

- `investigate_further` or `do_not_launch`.

---

## 23. Example: Low-Risk UI Change with Small Positive Lift

### User Question

> A low-risk checkout UI copy change increases checkout completion by 0.4%, with no movement in latency, refunds, or support tickets. Should we launch?

### Good Agent Reasoning

This is a low-risk, reversible product change. The evidence threshold is lower than for a ranking, ads, marketplace, or policy change.

The agent should ask:

- Did SRM and logging checks pass?
- Is the 0.4% lift practically meaningful at business scale?
- Was the experiment long enough to avoid day-of-week artifacts?
- Are refunds, cancellations, support tickets, and latency stable?
- Is the implementation easy to roll back?

Possible recommendation:

- If validity checks pass and the lift is meaningful at scale, launch or launch with monitoring.
- If uncertainty is wide and the lower bound includes material downside, investigate further.

Likely decision:

- `launch_with_monitoring` or `launch`.

---

## 24. Minimum Evidence Required for a Launch Memo

A launch memo should include the following sections.

---

### 24.1 Recommendation

State the decision label:

- `launch`
- `launch_with_monitoring`
- `partial_rollout`
- `investigate_further`
- `do_not_trust_result`
- `do_not_launch`
- `use_did_or_quasi_experiment`

---

### 24.2 Product Context

Describe:

- feature;
- target users;
- product surface;
- business goal;
- decision urgency;
- reversibility;
- risk tier.

---

### 24.3 Experiment Design

Include:

- treatment and control;
- randomization unit;
- sample size;
- duration;
- exposure definition;
- decision metric;
- success metrics;
- guardrail metrics;
- segment plan;
- pre-specified shipping criteria.

---

### 24.4 Results

Report:

- decision metric movement;
- practical effect size;
- uncertainty;
- success metric movement;
- guardrail movement;
- segment-level effects;
- long-term proxy metrics;
- diagnostic metric movement.

---

### 24.5 Validity Checks

Include:

- SRM check;
- logging check;
- assignment check;
- missing data check;
- contamination check;
- instrumentation check;
- novelty or seasonality concerns;
- peeking or early stopping concerns.

---

### 24.6 Risk Assessment

Discuss:

- user harm;
- business harm;
- trust and safety;
- marketplace or ecosystem effects;
- operational risk;
- reversibility;
- maintenance cost;
- brand or policy risk.

---

### 24.7 Next Steps

State:

- launch plan;
- partial rollout plan;
- additional analysis;
- rerun requirement;
- monitoring metrics;
- rollback thresholds;
- owner and timeline if available.

---

## 25. Response Template for the Agent

When answering a launch decision question, use this structure.

```text
Decision: [launch / launch_with_monitoring / partial_rollout / investigate_further / do_not_trust_result / do_not_launch / use_did_or_quasi_experiment]

Decision problem:
[Restate what decision is being made.]

Risk tier:
[low_risk_reversible / medium_risk_reversible / high_risk_reversible / high_risk_irreversible]

Metric hierarchy:
- Decision metric:
- Success metrics:
- Guardrail metrics:
- Diagnostic metrics:

Evidence assessment:
1. Trustworthiness checks:
2. Practical significance:
3. Uncertainty:
4. Guardrails:
5. Segment effects:
6. Long-term and ecosystem risk:

Recommendation:
[Clear final recommendation.]

Missing evidence:
- [Evidence 1]
- [Evidence 2]
- [Evidence 3]

Next steps:
- [Analysis or experiment step]
- [Monitoring or rollout step]
- [Rollback or decision threshold]
```

---

## 26. Evaluation Criteria for Agent Answers

This playbook should support both answer generation and answer evaluation.

A high-quality answer should:

- choose one allowed decision label;
- restate the decision problem clearly;
- classify the risk tier;
- define the metric hierarchy;
- check experiment trustworthiness before interpreting lift;
- distinguish statistical significance from practical significance;
- evaluate guardrails;
- analyze segment heterogeneity;
- consider long-term and ecosystem risk;
- state missing evidence;
- recommend concrete next steps;
- avoid overclaiming when evidence is incomplete.

Penalize an answer if it:

- recommends launch based only on one improved metric;
- treats a result with SRM, logging failure, or assignment failure as valid causal evidence;
- ignores guardrail deterioration;
- ignores harmed strategic segments;
- treats CTR, clicks, impressions, or time spent as sufficient launch evidence by themselves;
- fails to mention uncertainty;
- gives generic advice without a decision label;
- asks many clarifying questions without providing a provisional decision framing;
- cherry-picks favorable metrics while ignoring the stated decision metric;
- recommends broad launch when the evidence only supports limited rollout;
- recommends `partial_rollout` without specifying target segment, rollout size, monitoring metrics, and expansion criteria.

A strong answer should feel like a senior data scientist writing a concise launch review, not like a generic explanation of A/B testing.

---

## 27. Common Failure Modes

The agent should avoid these failure modes:

1. **Metric absolutism**

   Treating one metric as automatically decisive without understanding metric hierarchy.

2. **Statistical-significance-only reasoning**

   Recommending launch only because p < 0.05, without considering practical significance, guardrails, and risk.

3. **Ignoring experiment validity**

   Interpreting lift before checking SRM, assignment, exposure, and logging quality.

4. **Averages-only reasoning**

   Recommending launch based on average treatment effect while ignoring harmed strategic segments.

5. **Short-term engagement bias**

   Treating watch time, CTR, clicks, or sessions as automatically good even when they may damage retention, trust, safety, or monetization quality.

6. **Overusing partial rollout**

   Using partial rollout as a vague compromise without specifying target segment, traffic size, duration, monitoring, and expansion criteria.

7. **Overconfident answer under missing evidence**

   Giving a confident launch or no-launch recommendation when critical inputs are missing.

8. **Confusing observational correlation with causal evidence**

   Treating non-randomized results as if they came from a clean A/B test.

9. **Ignoring reversibility**

   Applying the same evidence standard to a small UI copy change and a major ranking, pricing, policy, or trust/safety change.

10. **Ignoring ecosystem effects**

   Failing to consider creator, seller, advertiser, marketplace, or content-quality consequences.

---

## 28. Final Rule

The agent should optimize for responsible decision quality, not for always giving a confident answer.

When evidence is strong and risk is controlled, recommend launch.

When evidence is promising but incomplete, recommend partial rollout or further investigation.

When the experiment is invalid, do not trust the result.

When the product change creates material harm, do not launch.

When the evidence is not randomized but the user asks a causal question, recommend a quasi-experimental design.

The best answer is not the most optimistic answer. The best answer is the one that makes the decision, evidence, risk, uncertainty, and next action explicit.