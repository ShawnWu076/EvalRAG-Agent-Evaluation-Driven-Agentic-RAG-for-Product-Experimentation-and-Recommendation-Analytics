# A/B Testing Playbook

This playbook defines how an evaluation-driven agent should design, audit, analyze, and interpret A/B tests.

It is written for an Agentic RAG system that behaves like a disciplined product analyst: it should not merely summarize experiment numbers, but translate evidence into a trustworthy decision process.

A good A/B testing answer should make clear:

- what causal question is being tested;
- whether randomization and exposure were valid;
- whether the observed result can be trusted;
- which metrics are decision metrics, success metrics, guardrails, diagnostics, and invariants;
- whether the effect is statistically reliable and practically meaningful;
- whether the result is safe across segments;
- whether the result may create long-term or ecosystem harm;
- whether a randomized experiment is appropriate, or whether quasi-experimental design is needed;
- and what the next responsible action should be.

The core rule is:

> **Validity first. Strategy second. Launch third.**

An experiment with invalid assignment, broken telemetry, SRM, biased exposure, or post-treatment filtering should not be used as causal evidence, even if the headline metric looks positive.

An experiment with a statistically significant lift should not automatically launch if the lift is shallow, strategically misaligned, harmful to a key segment, or damaging to guardrails.

An experiment with mixed metrics should not be treated as a failure by default. It should be interpreted through metric hierarchy, non-inferiority thresholds, practical magnitude, reversibility, and long-term risk.

---

## Quick Retrieval Summary

Use this playbook when the user asks about:

- designing an A/B test;
- interpreting A/B test results;
- checking experiment validity;
- choosing metrics;
- evaluating guardrails;
- deciding whether a result is trustworthy;
- diagnosing SRM, logging, exposure, randomization, or attribution issues;
- comparing treatment and control;
- handling heterogeneous treatment effects;
- deciding whether to use standard A/B testing, switchback testing, cluster randomization, geo experiments, or quasi-experimental methods;
- turning an experiment readout into a launch recommendation.

Default reasoning order:

1. Clarify the causal question and decision.
2. Identify product context and risk tier.
3. Define the experiment unit, assignment unit, exposure unit, and analysis unit.
4. Define the metric hierarchy.
5. Validate experiment trustworthiness before reading metric lifts.
6. Estimate treatment effects with uncertainty.
7. Evaluate practical magnitude.
8. Apply guardrail non-inferiority logic.
9. Scan pre-specified and strategic segments.
10. Check long-term, interference, and ecosystem risks.
11. Produce a decision-oriented readout with missing evidence and next steps.

---

## 1. Core Principle

A/B testing is a causal decision system, not a dashboard.

The purpose of an A/B test is not to find a metric that moved. The purpose is to estimate whether a product change caused a meaningful improvement under acceptable risk.

A strong A/B test requires:

- a clear hypothesis;
- valid randomization;
- correct exposure tracking;
- trustworthy logging;
- pre-specified metrics;
- practical effect thresholds;
- guardrail tolerances;
- segment protections;
- a planned stopping rule;
- and an explicit decision rule.

The agent should avoid both extremes:

- **metric optimism:** launching because one success metric improved;
- **metric pessimism:** blocking because one noisy secondary metric moved slightly negative.

The correct interpretation is:

> A treatment is successful only if it improves the intended objective by a meaningful amount while staying within the product’s risk budget.

---

## 2. Historical Use Patterns of A/B Testing

A/B testing practice has evolved from simple conversion comparisons into large-scale causal governance.

### 2.1 Early Web and E-Commerce Experiments

Early online A/B testing was often used for:

- page layout;
- button copy;
- checkout flows;
- signup forms;
- email subject lines;
- pricing display;
- merchandising modules.

The common decision pattern was simple:

> Does treatment increase conversion or click-through rate compared with control?

This was useful for low-risk, reversible changes, but weak for strategic product decisions. It often over-weighted short-term conversion and under-weighted retention, trust, operational cost, and long-term user value.

### 2.2 Mature Experimentation Platforms

Large technology companies pushed experimentation toward platformized discipline:

- centralized assignment;
- automatic metric computation;
- SRM detection;
- invariant checks;
- standard metric libraries;
- experiment scorecards;
- pre-launch ramping;
- alerting;
- post-experiment diagnostics;
- decision review.

The main lesson:

> At scale, the hard part is not computing a p-value. The hard part is ensuring that the comparison is trustworthy and decision-relevant.

### 2.3 Marketplace and Networked Systems

Marketplaces, social products, auctions, feeds, and recommender systems exposed a limitation of simple user-level A/B testing:

> One unit’s treatment can affect another unit’s outcome.

Examples:

- treating sellers can affect buyer choices;
- changing ad ranking can affect advertiser competition;
- changing recommendations can redistribute attention across creators;
- changing prices can alter the behavior of nearby competitors;
- changing a delivery or rideshare algorithm can change system state over time.

In these settings, the agent should consider:

- cluster randomization;
- geo experiments;
- switchback experiments;
- marketplace-level holdouts;
- budget-split designs;
- interference-aware estimators;
- longer ecosystem monitoring.

### 2.4 Modern ML, Ranking, and Recommendation Experiments

For ML systems, online experiments usually sit after offline evaluation.

A model should not go online only because offline metrics improved. The online test must check:

- user outcome metrics;
- latency;
- reliability;
- fairness or segment harm;
- content quality;
- retention;
- feedback loops;
- exploitation of shallow proxies;
- long-term model-induced behavior change.

Offline AUC, NDCG, precision, recall, or loss improvement is useful, but it is not a launch decision by itself.

### 2.5 Agentic Analytics and Automated Experiment Readouts

For an automated data-analysis agent, A/B testing should become an executable reasoning protocol.

The agent should:

- retrieve the correct playbook;
- identify the decision problem;
- inspect data quality first;
- run standard validity checks;
- compute or request missing effect estimates;
- classify metrics by decision role;
- evaluate tradeoffs;
- produce an auditable readout;
- refuse to overclaim when evidence is invalid or incomplete.

The agent should behave like a senior analyst writing a launch review, not like a generic statistics explainer.

---

## 3. A/B Test Status Labels

The agent should assign exactly one primary experiment status label before giving a launch recommendation.

Allowed experiment status labels:

- `ready_to_read`
- `do_not_trust_result`
- `inconclusive`
- `positive_aligned`
- `negative_aligned`
- `mixed_tradeoff`
- `segment_specific`
- `needs_longer_readout`
- `use_quasi_experiment`

### 3.1 `ready_to_read`

Use when:

- assignment was valid;
- exposure logging is consistent;
- SRM checks pass;
- metric logging is complete enough;
- no major instrumentation or pipeline issue is detected;
- the planned analysis window is valid.

This label does not mean the treatment succeeded. It only means the experiment can be interpreted.

### 3.2 `do_not_trust_result`

Use when the experiment should not be interpreted as causal evidence.

Examples:

- SRM;
- assignment bug;
- unstable bucketing;
- treatment/control contamination;
- exposure definition mismatch;
- differential logging;
- missing telemetry;
- duplicated users or events;
- post-treatment filtering;
- bot/spam imbalance;
- metric pipeline change during the test;
- peeking-driven early stopping without sequential correction.

When using this label, the agent should not discuss the observed lift as if it were causal.

### 3.3 `inconclusive`

Use when the test is valid but does not provide enough evidence to support a product decision.

Examples:

- confidence interval includes meaningful upside and downside;
- underpowered experiment;
- effect is too small relative to MDE;
- metric movement is directionally positive but uncertain;
- guardrails are noisy;
- duration is too short for the intended outcome.

### 3.4 `positive_aligned`

Use when:

- the decision metric improves;
- the effect is practically meaningful;
- confidence interval excludes material downside;
- guardrails are stable or within tolerance;
- strategic segments are not harmed;
- long-term risk is low or monitored.

### 3.5 `negative_aligned`

Use when:

- the decision metric declines;
- the treatment fails to improve the intended objective;
- the effect contradicts the hypothesis;
- or the expected product value is lower than control.

### 3.6 `mixed_tradeoff`

Use when the test is valid but metrics conflict.

Examples:

- activation improves but retention declines;
- revenue rises but advertiser ROI falls;
- CTR improves but satisfaction declines;
- engagement rises but trust/safety reports increase;
- conversion rises but refunds or cancellations rise.

This label requires metric hierarchy and guardrail tolerance analysis.

### 3.7 `segment_specific`

Use when the average effect hides meaningful heterogeneity.

Examples:

- new users benefit but existing users are harmed;
- one geography improves while another degrades;
- desktop improves while mobile worsens;
- buyers benefit while sellers are harmed;
- power users are harmed while casual users improve.

The agent should not recommend broad rollout unless harmed strategic segments are protected.

### 3.8 `needs_longer_readout`

Use when short-term evidence is positive but the product risk is long-term.

Examples:

- habit formation;
- user fatigue;
- content quality degradation;
- creator/seller incentive shifts;
- ad saturation;
- subscription churn;
- marketplace liquidity;
- trust and safety spillovers.

### 3.9 `use_quasi_experiment`

Use when the question is causal, but clean randomized evidence is unavailable or inappropriate.

Examples:

- policy rollout by geography;
- eligibility rule change;
- pricing change applied by market;
- marketplace interference;
- self-selected exposure;
- historical product launch without randomization.

Possible methods:

- Difference-in-Differences;
- regression discontinuity;
- synthetic control;
- matching or weighting;
- interrupted time series;
- geo experiment;
- switchback experiment;
- instrumental variables.

### 3.10 Status Precedence Rules

When multiple status labels are plausible, choose the highest-priority status in this order:

1. `do_not_trust_result`
   - Use if assignment, exposure, SRM, logging, or post-treatment filtering invalidates causal interpretation.
   - This overrides all metric movement.

2. `use_quasi_experiment`
   - Use if the evidence is observational, randomization is unavailable, or interference makes standard A/B invalid.

3. `segment_specific`
   - Use if average impact is positive but a strategic or protected segment is materially harmed.

4. `mixed_tradeoff`
   - Use if decision metric improves but hard/semi-hard guardrails fail or business tradeoffs are unresolved.

5. `needs_longer_readout`
   - Use if short-term evidence is positive but delayed harm, fatigue, churn, ecosystem feedback, or trust risk is plausible.

6. `inconclusive`
   - Use if validity passes but uncertainty is too large for decision-making.

7. `positive_aligned` / `negative_aligned`
   - Use only after validity, guardrails, segments, and long-term checks are resolved.

---

## 4. Experiment Design Contract

Every A/B test should have a design contract before data is read.

The contract should define:

| Field | Required Content |
|---|---|
| Decision | What decision will the experiment inform? |
| Hypothesis | What mechanism should the treatment change? |
| Control | What is the baseline experience? |
| Treatment | What exactly changes? |
| Target population | Who is eligible? |
| Randomization unit | User, session, account, device, household, listing, seller, geography, time block, cluster, etc. |
| Assignment mechanism | How is treatment assigned and persisted? |
| Exposure definition | What counts as being exposed to treatment? |
| Analysis population | Assigned users, triggered users, exposed users, eligible users, or another set? |
| Primary decision metric | The metric closest to the product objective. |
| Success metrics | Metrics expected to improve if the hypothesis is correct. |
| Guardrail metrics | Metrics that must not degrade beyond tolerance. |
| Invariant metrics | Metrics that should not differ between variants if the test is valid. |
| Segment plan | Pre-specified segments and strategic segments to scan. |
| MDE / practical threshold | Minimum effect size worth acting on. |
| Guardrail tolerance | Maximum acceptable deterioration. |
| Test duration | Planned runtime and readout windows. |
| Stopping rule | Fixed horizon, sequential, Bayesian, or safety-only monitoring. |
| Ramp plan | Initial exposure, ramp schedule, and rollback conditions. |
| Long-term plan | Whether holdout, delayed readout, or post-launch monitoring is required. |

Bad design pattern:

> We launched a test, looked at all metrics, and picked the one that improved.

Better design pattern:

> We pre-specified activation as the decision metric, retention and complaints as guardrails, latency as an infrastructure guardrail, new/existing users as mandatory segments, and rollback thresholds before reading results.

### 4.1 Machine-Readable Experiment Spec

The agent should convert every experiment request into a structured contract before analysis.

```yaml
experiment_id:
decision:
hypothesis:
product_surface:
risk_tier: low | medium | high
reversibility: reversible | partially_reversible | irreversible

design:
  control:
  treatment:
  target_population:
  randomization_unit:
  assignment_unit:
  exposure_unit:
  analysis_unit:
  assignment_mechanism:
  exposure_definition:
  duration:
  planned_stopping_rule:
  ramp_plan:

metrics:
  decision_metric:
  success_metrics:
  guardrail_metrics:
    - name:
      harm_direction: higher_is_worse | lower_is_worse
      harm_margin:
      hard_or_soft: hard | soft
  diagnostic_metrics:
  invariant_metrics:

validity:
  srm_check_required: true
  exposure_audit_required: true
  invariant_balance_required: true
  post_treatment_filtering_allowed: false

segments:
  prespecified:
  strategic:
  protected_or_sensitive:

decision_rule:
  minimum_practical_lift:
  guardrail_noninferiority_required: true
  segment_harm_policy:
  long_term_holdout_required:

---

## 5. Metric Hierarchy

The agent must classify metrics before interpreting results.

Not all metrics have equal decision weight.

### 5.1 Decision Metric / OEC

The decision metric, or overall evaluation criterion, is the metric or metric bundle that best represents the product objective.

A good decision metric should be:

- aligned with durable user or business value;
- sensitive enough for experimentation;
- difficult to game through shallow behavior;
- interpretable;
- connected to the stated hypothesis;
- meaningful at product scale.

Examples:

| Product Area | Possible Decision Metric |
|---|---|
| Onboarding | Activated users, qualified first action, D7 retention |
| Checkout | Completed purchase, net conversion, margin-adjusted conversion |
| Subscription | Paid conversion, trial-to-paid rate, churn-adjusted LTV |
| Recommendations | Qualified engagement, retention, satisfaction, successful sessions |
| Search | Successful search, downstream conversion, reformulation reduction |
| Ads | Revenue quality, advertiser ROI, long-term advertiser spend |
| Marketplace | Quality-adjusted GMV, liquidity, buyer/seller retention |
| Trust & Safety | Harmful exposure reduction, enforcement accuracy, appeal-adjusted harm |

### 5.2 Success Metrics

Success metrics should move if the product hypothesis is correct.

Examples:

- activation rate;
- checkout completion;
- revenue per user;
- first successful session;
- qualified watch time;
- search success;
- seller response rate;
- buyer conversion;
- advertiser conversion;
- useful answer rate.

A success metric should not be treated as decisive if it is far away from durable value.

### 5.3 Guardrail Metrics

Guardrails are metrics that must not materially deteriorate.

Examples:

- retention;
- churn;
- complaint rate;
- hide/report/block rate;
- refund rate;
- cancellation rate;
- crash rate;
- latency;
- error rate;
- support tickets;
- content quality;
- trust and safety violations;
- advertiser ROI;
- seller retention;
- marketplace liquidity;
- fairness metrics.

Guardrails are not always expected to improve. Often they must satisfy non-inferiority:

> The treatment is acceptable only if guardrail deterioration is smaller than the maximum acceptable harm.

### 5.4 Diagnostic Metrics

Diagnostic metrics explain mechanism but should not usually drive launch alone.

Examples:

- CTR;
- impressions;
- scroll depth;
- session count;
- notification opens;
- time spent on a narrow surface;
- number of recommendations shown;
- query reformulations;
- click depth.

Diagnostic lift is not enough if the decision metric is flat or guardrails degrade.

### 5.5 Invariant Metrics

Invariant metrics should not differ between variants if the experiment is healthy.

Examples:

- assigned user counts;
- pre-treatment user attributes;
- geography mix;
- platform mix;
- app version mix;
- eligibility counts;
- pre-period activity;
- account age;
- device family;
- logged exposure opportunity counts when expected to be equal.

Invariant failures indicate possible invalidity.

---

## 6. Validity First Checklist

The agent must validate experiment trustworthiness before interpreting metric movement.

### 6.1 Pre-Experiment Validity

Check before launch:

- hypothesis is explicit;
- randomization unit matches the product mechanism;
- assignment is persistent;
- eligibility is deterministic;
- exposure is well-defined;
- metrics are already logged or instrumented consistently;
- guardrails and invariants are defined;
- power and MDE are estimated;
- duration covers relevant weekly or seasonal cycles;
- stopping rule is specified;
- overlapping experiment policy is understood;
- ramp and rollback plan exists.

### 6.2 During-Experiment Monitoring

Monitor while the test is running:

- SRM;
- assignment counts;
- exposure counts;
- treatment load failure;
- logging volume;
- event schema changes;
- severe latency/crash/error guardrails;
- bot/spam anomalies;
- ramp configuration;
- treatment availability by platform/app version;
- experiment collisions if interactions are likely.

During-experiment monitoring should be used mainly for safety and validity, not opportunistic success declaration.

### 6.3 Post-Experiment Validity

Check before analysis:

- SRM on assigned population;
- SRM on triggered/exposed population if triggered analysis is used;
- exposure consistency across variants;
- no post-treatment filtering;
- no differential missingness;
- no duplicated users or events;
- no metric logging parity issue;
- no bot/spam imbalance;
- no treatment/control contamination;
- no instrumentation change during the test;
- no data pipeline change during the test;
- no sample censoring that differs by variant;
- invariant metrics are balanced;
- experiment ran for the planned analysis window.

### 6.4 SRM Rule

If SRM is detected, the default status is:

> `do_not_trust_result`

Do not interpret the observed treatment lift until the root cause is diagnosed.

Possible SRM root causes:

- randomization bug;
- ramp misconfiguration;
- variant self-selection;
- treatment load failure;
- bot/spam filtering;
- triggered analysis bias;
- logging loss;
- eligibility mismatch;
- client-side bucketing issue;
- app-version-specific bug;
- exposure opportunity mismatch.

### 6.5 Exposure Consistency Audit

The agent should distinguish:

- **assigned:** unit was randomized;
- **eligible:** unit met experiment eligibility criteria;
- **triggered:** unit reached the condition for inclusion;
- **exposed:** unit actually saw or received treatment;
- **analyzed:** unit appears in the metric dataset.

Required audit:

```text
assigned_count >= eligible_count >= triggered_count >= exposed_count >= analyzed_count
```

Not every test has all levels, but the agent should check whether counts drop differently by variant.

Differential drop-off can create bias.

### 6.6 Post-Treatment Filtering Rule

Do not filter on variables affected by treatment unless the estimand explicitly requires it and the bias is understood.

Bad:

> Analyze only users who clicked the new module.

Better:

> Analyze all assigned or triggered users, and use click behavior as a diagnostic mechanism metric.

---

## 7. Statistical Interpretation

### 7.1 Default Estimand

The default estimand should be the intent-to-treat effect when assignment is valid:

```text
ITT = E[Y | assigned treatment] - E[Y | assigned control]
```

Use treatment-on-treated only when exposure is not guaranteed and the assumptions are explicitly stated.

### 7.2 Difference in Means or Proportions

For many metrics:

```text
effect = mean_treatment - mean_control
relative_lift = effect / mean_control
```

Report:

- control mean;
- treatment mean;
- absolute effect;
- relative effect;
- confidence interval;
- p-value or posterior probability if used;
- practical threshold;
- sample size;
- analysis window.

### 7.3 Ratio Metrics

For ratio metrics such as revenue per session or clicks per impression, the agent should be careful.

Common approaches:

- delta method;
- bootstrap;
- user-level aggregation before comparison;
- cluster-robust standard errors if observations are correlated;
- CUPED or regression adjustment if appropriate.

Avoid treating numerator and denominator events as independent when they are not.

### 7.4 Practical Significance

Statistical significance is not enough.

The agent should ask:

- Is the effect large enough to matter?
- Does it exceed the pre-specified MDE or business threshold?
- Does the lower confidence bound still support action?
- Is the expected value worth engineering, operational, or maintenance cost?
- Does the lift improve durable value or only a shallow proxy?

Decision rule example:

```text
Launch-positive evidence exists only if:
lower_CI(decision_metric_effect) > minimum_practical_lift
and all hard guardrails satisfy non-inferiority.
```

For low-risk reversible changes, the threshold may be smaller.

For high-risk or irreversible changes, the threshold should be stricter.

### 7.5 Non-Inferiority for Guardrails

For guardrails, the question is often not:

> Did the guardrail move?

The better question is:

> Did the guardrail get worse by more than the maximum acceptable harm?

Let deterioration be positive when worse:

```text
guardrail_deterioration = treatment_guardrail - control_guardrail
```

For bad-outcome metrics such as crash rate or refund rate:

```text
Pass non-inferiority if upper_CI(guardrail_deterioration) <= harm_margin
```

For good-outcome guardrails such as retention:

```text
Pass non-inferiority if lower_CI(treatment - control) >= -harm_margin
```

Examples:

| Guardrail | Harm Margin |
|---|---|
| Page latency | +20 ms |
| Crash rate | +0.10 percentage points |
| Refund rate | +0.20 percentage points |
| D7 retention | -0.30 percentage points |
| Complaint rate | +0.05 percentage points |
| Advertiser ROI | -1.00% |
| Seller retention | -0.25 percentage points |

If a hard guardrail fails, do not recommend broad launch.

### 7.6 Multiple Testing

Segment scans and many metrics increase false positives.

The agent should separate:

- pre-specified confirmatory tests;
- exploratory diagnostics;
- segment scans;
- post-hoc investigations.

Possible controls:

- Holm-Bonferroni;
- Benjamini-Hochberg FDR;
- hierarchical testing;
- metric family gating;
- pre-specified segment priority;
- replication test.

Do not overreact to one noisy segment unless the segment is strategically important and the effect is practically large.

### 7.7 Peeking and Sequential Testing

If the team repeatedly checks success metrics and stops when results look good, ordinary p-values may be invalid.

The agent should ask:

- Was the test fixed-horizon?
- Was early stopping pre-specified?
- Was an anytime-valid or sequential method used?
- Were interim checks for safety only?
- Did the team stop because the result became favorable?

If unplanned peeking occurred, prefer:

- `inconclusive`;
- rerun;
- sequentially valid analysis;
- or conservative interpretation.

### 7.8 Power and MDE

If a test finds no significant harm, this does not prove safety.

The agent should inspect:

- sample size;
- variance;
- MDE;
- confidence interval width;
- whether the experiment was powered for guardrails;
- whether rare harms require larger samples.

For high-risk guardrails, absence of evidence is not evidence of absence.

### 7.9 Sensitivity Optimization (CUPED)
When an experiment is underpowered or results are `inconclusive`, use CUPED (Controlled-experiment Using Pre-Experiment Data) to reduce variance and increase sensitivity.

* **Prescriptive Rule**: Use pre-experiment data (e.g., the 2 weeks prior to launch) as a covariate to adjust the post-launch metric.
* **Constraint**: Never use covariates that could be affected by the treatment.
* **Output Requirement**: If CUPED is applied, the Agent must report both the raw lift and the variance-adjusted lift to ensure transparency.

Never adjust for post-treatment variables when estimating the total treatment effect.

### 7.10 Handling Outliers and Skewed Distributions
For metrics with long-tailed distributions (e.g., Revenue, Order Value, Latency), mean-based estimates can be heavily biased by a small number of extreme units.

* **Standard Procedure**: Always check P50 (median), P90, and P99 alongside the mean to detect skewness.
* **Winsorization/Capping**: If extreme outliers are detected (e.g., bots or "whales"), apply pre-specified capping (Winsorization) at the 99th percentile to reduce variance.
* **Log Transformation**: For highly skewed monetary metrics, consider analyzing the log-transformed values to stabilize variance, while remaining cautious about interpretability.

### 7.11 Statistical Method Router

The agent should choose the estimation method based on metric type and data structure.

| Metric Type | Examples | Preferred Method | Notes |
|---|---|---|---|
| Binary user-level metric | conversion, activation, churn | difference in proportions / logistic regression | Report absolute pp change and relative lift |
| Continuous user-level metric | revenue per user, sessions per user | difference in means / regression adjustment | Use robust SE if skewed |
| Ratio metric | clicks per impression, revenue per session | delta method, bootstrap, or user-level aggregation | Do not treat numerator and denominator as independent |
| Count metric | number of sessions, orders | Poisson/negative binomial or user-level mean | Check overdispersion |
| Long-tailed metric | revenue, latency, order value | bootstrap, winsorization, quantile readout | Report P50/P90/P99 |
| Clustered metric | seller, geo, classroom, marketplace | cluster-robust SE or cluster-level analysis | Match SE to randomization unit |
| Repeated observations | sessions nested in users | user-level aggregation or mixed model | Avoid event-level false precision |
| Rare guardrail | crash, abuse, fraud, policy violation | longer window, exact methods, Bayesian shrinkage, or pooled monitoring | No significant harm is not proof of safety |

---

## 8. Segment Scan Framework

Averages can hide harm.

The agent should scan:

- new vs existing users;
- high-value vs low-value users;
- power users vs casual users;
- paid vs free users;
- creators vs consumers;
- buyers vs sellers;
- advertisers vs users;
- geographies;
- platforms;
- app versions;
- acquisition channels;
- content categories;
- user intent groups;
- risk/safety groups;
- accessibility-sensitive users;
- language or locale;
- device class.

### 8.1 Segment Scan Rules

The agent should:

1. Start with pre-specified segments.
2. Add strategic segments relevant to product risk.
3. Check sample size and uncertainty.
4. Distinguish exploratory findings from confirmatory findings.
5. Avoid broad launch if a protected or strategic segment is materially harmed.
6. Avoid overreacting to tiny noisy subgroups.
7. Recommend targeted rollout if benefit is segment-specific and harm can be avoided.

### 8.2 Simpson’s Paradox Warning

The agent should check whether the aggregate effect differs from segment-level effects.

Example:

- overall conversion improves;
- mobile conversion worsens;
- desktop conversion improves strongly;
- mobile is the strategic growth surface.

Averages are not enough.

### 8.2.1 Automated Paradox Detection

The Agent is required to automatically flag "Directional Flip":
* **Rule**: If the aggregate effect is `positive` but a strategic segment (e.g., Mobile Users, New Users) shows a statistically significant `negative` effect, the Agent must downgrade the status to `segment_specific` and block broad launch.

### 8.3 Segment Decision Patterns

| Pattern | Interpretation | Action |
|---|---|---|
| Broad positive, no segment harm | Strong evidence | Launch or launch with monitoring |
| Positive only in target segment | Targeted value | Partial rollout to target segment |
| Average positive, strategic segment harmed | Hidden risk | Partial rollout or investigate further |
| Average flat, one strategic segment strongly positive | Potential opportunity | Segment-specific experiment |
| Many noisy segment movements | Multiple testing risk | Treat as exploratory |
| Harm in vulnerable or protected segment | High-risk | Do not launch broadly |

---

## 9. Long-Term and Ecosystem Risk

Short tests can miss slow harm.

The agent should check for:

- novelty effects;
- user fatigue;
- content quality degradation;
- trust erosion;
- subscription churn;
- creator or seller incentive shifts;
- advertiser ROI deterioration;
- marketplace imbalance;
- cannibalization of existing surfaces;
- ranking feedback loops;
- user learning or strategic behavior;
- policy or brand risk.

### 9.1 Long-Term Holdout

Use a long-term holdout when:

- the treatment affects ranking, recommendations, pricing, policy, incentives, ads, or trust;
- short-term and long-term metrics may diverge;
- novelty or fatigue is likely;
- the feature may affect user habits;
- the ecosystem may adapt over time.

A long-term holdout should specify:

- holdout population;
- holdout duration;
- protected metrics;
- expansion rules;
- rollback thresholds;
- whether holdout can remain as an evergreen measurement cell.

### 9.2 Delayed Readout Metrics

Examples:

- D7, D14, D28 retention;
- churn;
- reactivation;
- repeat purchase;
- repeat booking;
- creator posting retention;
- seller response quality;
- advertiser repeat spend;
- user trust surveys;
- support tickets;
- refund and cancellation rates;
- policy violations;
- content quality distribution.

### 9.3 User Fatigue

Watch for:

- notification opt-outs;
- lower open rates over time;
- higher complaint rates;
- reduced session quality;
- lower retention after initial lift;
- surface-level engagement replacing deeper engagement.

Short-term lift with fatigue is not durable value.

---

## 10. Interference-Aware Design

Standard user-level A/B tests assume one unit’s treatment does not affect another unit’s outcome.

This assumption can fail in:

- marketplaces;
- social networks;
- recommendations;
- feed ranking;
- ads auctions;
- delivery or rideshare matching;
- creator ecosystems;
- seller competition;
- inventory allocation;
- pricing systems;
- networked communication products.

### 10.1 Interference Symptoms

Possible signs:

- treatment changes supply available to control users;
- treatment redistributes traffic among creators or sellers;
- user-level test moves marketplace-wide prices or inventory;
- control users interact with treated users;
- ads auction outcomes depend on both treatment and control participants;
- total platform metrics differ from average user-level estimates;
- effects vary by geography saturation or supply-demand balance.

### 10.2 Design Options

| Situation | Better Design |
|---|---|
| Time-dependent operations policy | Switchback experiment |
| Marketplace pricing or seller intervention | Cluster randomization or geo experiment |
| Ads auction change | Auction-level or budget-split design |
| Recommendation system with item spillovers | Cluster randomization or item/user bipartite design |
| Policy rollout by region | Difference-in-Differences or geo experiment |
| Inventory or supply constraints | Market-level randomization |
| Network feed change | Cluster randomization by graph/community |

### 10.3 When to Use Switchback Experiments

Use switchback when:

- treatment changes system state over time;
- user-level randomization is infeasible;
- supply/demand conditions vary by time;
- the product has operational constraints;
- the same market can alternate between control and treatment.

Examples:

- delivery matching;
- rideshare dispatch;
- surge pricing;
- inventory allocation;
- ads pacing;
- logistics routing.

### 10.4 When to Use Cluster Randomization

Use cluster randomization when:

- units interact strongly;
- treatment spillovers follow geography, graph, marketplace category, or seller/buyer clusters;
- individual randomization would contaminate control.

Examples:

- social graph features;
- marketplace seller tools;
- creator recommendation changes;
- local service marketplaces;
- pricing experiments.

### 10.5 Interference Decision Logic
The Agent must use the following "Interference Detection" logic before recommending a standard user-level A/B test:

* **Supply/Price Constraint**: If the treatment changes the price or availability of a shared resource (e.g., delivery drivers, hotel inventory), **Standard A/B is Forbidden**. Use **Switchback** or **Geo-testing**.
* **Social/Network Effect**: If the treatment changes how users interact (e.g., messaging, social sharing), use **Cluster Randomization**.
* **Marketplace Competition**: If treating one seller harms another seller's visibility, use **Market-level** or **Cluster** designs.

---

## 11. Scenario-Specific Playbooks

### 11.1 Low-Risk UI or Copy Change

Examples:

- button text;
- layout tweak;
- tooltip;
- small visual change;
- minor onboarding copy.

Recommended design:

- user-level randomization;
- fixed-horizon test;
- primary metric tied to the surface;
- basic guardrails.

Metrics:

- decision: conversion or task completion;
- guardrails: latency, error rate, support tickets, refund/cancellation if relevant;
- diagnostics: clicks, scroll depth.

Interpretation:

- lower evidence threshold is acceptable if the change is reversible;
- still require SRM and logging checks;
- launch if effect is meaningful at scale and guardrails are stable.

### 11.2 Onboarding or Activation

Examples:

- new-user tutorial;
- setup flow;
- first-action prompt;
- personalization onboarding.

Metrics:

- decision: activated user rate, qualified first action, D7 retention;
- guardrails: early churn, support tickets, account deletion, latency;
- diagnostics: step completion, click rate, form completion.

Pitfalls:

- optimizing signup completion while lowering activated retention;
- helping new users while confusing existing users;
- novelty effect.

Recommended action:

- segment new vs existing users;
- require early retention readout;
- consider partial rollout to new users only.

### 11.3 Checkout, Subscription, or Conversion Funnel

Examples:

- checkout UI;
- pricing presentation;
- payment flow;
- subscription trial design.

Metrics:

- decision: net conversion, paid conversion, margin-adjusted revenue;
- guardrails: refunds, cancellations, chargebacks, support tickets, churn;
- diagnostics: click-through, step completion, payment retries.

Pitfalls:

- increasing short-term conversion through confusing pricing;
- increasing purchases that later refund;
- improving trial start but worsening paid conversion.

Recommended action:

- include delayed refund/cancellation readout;
- protect trust and pricing clarity;
- use non-inferiority for refunds and support contacts.

### 11.4 Recommendations, Search, Feed, or Ranking

Examples:

- feed ranking model;
- search ranking;
- recommendation module;
- personalization model.

Metrics:

- decision: successful sessions, long-term retention, satisfaction, qualified engagement;
- guardrails: hides, reports, low-quality exposure, diversity, latency, creator health;
- diagnostics: CTR, impressions, dwell time, scroll depth.

Pitfalls:

- CTR lift from clickbait;
- engagement lift from low-quality content;
- content diversity collapse;
- creator incentive distortion;
- retention harm hidden by short-term engagement.

Recommended action:

- never launch on CTR alone;
- run segment scan by user intent and content category;
- use long-term holdout when ranking incentives may shift;
- consider interference-aware design if attention is redistributed across creators/items.

### 11.5 Ads and Monetization

Examples:

- ad ranking;
- ad load;
- auction model;
- sponsored placement.

Metrics:

- decision: revenue quality, long-term revenue, advertiser ROI;
- guardrails: user retention, ad fatigue, advertiser conversion, complaint rate, page latency;
- diagnostics: CTR, fill rate, impressions, CPM.

Pitfalls:

- short-term revenue increases by damaging advertiser ROI;
- ad load increases churn;
- auction changes distort advertiser mix.

Recommended action:

- treat advertiser ROI as a hard or semi-hard guardrail;
- monitor user fatigue;
- check advertiser segment effects;
- use longer readout for advertiser retention.

### 11.6 Marketplace Experiments

Examples:

- seller pricing tool;
- buyer ranking;
- marketplace fee;
- host/driver/seller incentive;
- matching algorithm.

Metrics:

- decision: quality-adjusted GMV, liquidity, completed transactions, balanced marketplace health;
- guardrails: buyer retention, seller retention, cancellation rate, response time, refunds;
- diagnostics: clicks, messages, listing views, offer rate.

Pitfalls:

- buyer gain at seller expense;
- seller tool affects competitor sellers;
- marketplace-wide price shifts;
- individual-level randomization underestimates or overestimates total effect.

Recommended action:

- consider cluster randomization or geo experiments;
- scan buyer and seller segments separately;
- monitor liquidity and distributional effects;
- avoid optimizing one side of the marketplace alone.

### 11.7 Notifications and Messaging

Examples:

- push notification timing;
- email frequency;
- lifecycle campaigns;
- recommendation notifications.

Metrics:

- decision: retained engagement, useful action rate, reactivation;
- guardrails: opt-outs, unsubscribe, spam reports, churn, complaint rate;
- diagnostics: open rate, click rate.

Pitfalls:

- short-term opens with long-term fatigue;
- increased sessions with lower satisfaction;
- notification overload.

Recommended action:

- use frequency caps;
- monitor fatigue over time;
- require opt-out and unsubscribe guardrails;
- use long-term holdout for high-volume messaging.

### 11.8 Pricing, Policy, Privacy, or Trust/Safety

Examples:

- pricing rule;
- privacy feature;
- content moderation policy;
- account enforcement;
- underage user experience;
- creator monetization rule.

Metrics:

- decision: policy goal, trust/safety outcome, compliant value;
- guardrails: appeals, complaints, legal/policy risk, retention, false positives, false negatives;
- diagnostics: enforcement volume, review rate.

Pitfalls:

- average treatment effect hides harm to vulnerable users;
- irreversible trust damage;
- compliance risk;
- delayed behavioral response.

Recommended action:

- high evidence threshold;
- stakeholder review;
- conservative guardrails;
- partial rollout or quasi-experiment when randomization is not appropriate;
- long-term monitoring.

### 11.9 Infrastructure or Performance Experiments

Examples:

- latency optimization;
- caching change;
- backend migration;
- model serving change;
- database or API change.

Metrics:

- decision: latency, reliability, cost, error rate;
- guardrails: conversion, retention, crash rate, data correctness;
- diagnostics: CPU, memory, throughput, cache hit rate.

Pitfalls:

- performance improves while correctness breaks;
- small latency gain not worth complexity;
- uneven impact by platform or geography.

Recommended action:

- use hard guardrails for correctness and error rate;
- segment by platform, region, app version;
- include rollback thresholds.

### 11.10 Agentic RAG or Automated Analytics Product

Examples:

- new retrieval strategy;
- reranker;
- answer-generation prompt;
- citation policy;
- tool-use planner;
- launch-decision agent;
- recommendation analytics agent.

Metrics:

- decision: task success, answer groundedness, decision usefulness, analyst time saved;
- success: retrieval hit rate, citation coverage, correct decision label, useful next steps;
- guardrails: unsupported claims, hallucination rate, wrong causal interpretation, latency, cost, unsafe recommendation;
- diagnostics: number of retrieved chunks, query rewrite count, tool calls, reranker score.

Pitfalls:

- optimizing answer fluency while reducing factual grounding;
- improving average success while failing high-risk launch decisions;
- retrieval succeeds but synthesis misuses evidence;
- agent recommends launch without validity checks.

Recommended action:

- evaluate both retrieval and decision quality;
- include adversarial cases such as SRM, guardrail failure, segment harm, observational evidence, and interference;
- require evidence citations;
- score whether the agent follows the required reasoning order.

### 11.11 Offline-to-Online Bridge for Agentic RAG

Before online A/B testing, agentic RAG changes should pass offline evaluation.

Offline evaluation should include:

- retrieval hit rate;
- citation coverage;
- answer faithfulness;
- unsupported claim rate;
- correct decision label rate;
- tool-use success rate;
- latency and cost;
- robustness on adversarial cases.

Online A/B testing should not be launched only because offline metrics improve.

Online metrics should include:

- analyst task success;
- decision usefulness;
- correction rate by human reviewers;
- time saved;
- downstream decision accuracy;
- user trust or satisfaction;
- unsupported recommendation rate;
- unsafe launch recommendation rate.

If offline retrieval improves but decision quality worsens, do not launch.
If answer fluency improves but faithfulness worsens, do not launch.
If latency/cost rises beyond guardrail tolerance, require tradeoff review.

---

## 12. Required Agent Reasoning Order

For every A/B testing question, use this order.

### Step 1: Translate the User Request into a Decision Problem

Examples:

- “Did this experiment work?”
- “Should we launch?”
- “Why did metrics conflict?”
- “Can we trust this result?”
- “What should we test next?”
- “Is this causal?”

The agent should restate the decision problem explicitly.

### Step 2: Identify Product Context

Infer or ask:

- product surface;
- treatment;
- target population;
- business objective;
- risk tier;
- reversibility;
- likely long-term risk.

### Step 3: Define the Experiment Design

Identify:

- control;
- treatment;
- randomization unit;
- exposure definition;
- analysis unit;
- duration;
- sample size;
- planned stopping rule.

If these are missing, the agent should flag the readout as provisional.

### Step 4: Define Metric Hierarchy

Classify:

- decision metric;
- success metrics;
- guardrails;
- diagnostics;
- invariants;
- long-term proxies.

### Step 5: Run Validity Checks

Before reading lift:

- SRM;
- assignment consistency;
- exposure consistency;
- logging completeness;
- contamination;
- post-treatment filtering;
- invariant balance;
- missingness;
- duplicate events;
- instrumentation changes;
- bot/spam imbalance;
- peeking and stopping rule.

If serious validity checks fail, use `do_not_trust_result`.

### Step 6: Estimate Effects

Report:

- treatment mean;
- control mean;
- absolute difference;
- relative lift;
- confidence interval;
- p-value or posterior if available;
- sample size;
- practical threshold.

### Step 7: Evaluate Practical Magnitude

Ask:

- is the effect meaningful at scale?
- does it exceed the pre-specified MDE?
- is lower-bound impact still acceptable?
- does it justify cost and complexity?

### Step 8: Apply Guardrail Logic

For each guardrail:

- define harm direction;
- define harm margin;
- inspect confidence interval;
- classify as pass, fail, or underpowered.

### Step 9: Scan Segments

Check:

- pre-specified segments;
- strategic risk segments;
- harmed segments;
- sample size and uncertainty;
- whether targeted rollout is possible.

### Step 10: Check Long-Term and Interference Risk

Ask:

- is the experiment too short?
- can novelty or fatigue explain results?
- are there network, marketplace, ranking, or auction spillovers?
- is individual randomization appropriate?
- is a long-term holdout needed?

### Step 11: Mechanism Consistency Check

Before the final recommendation, the Agent must perform a "Why" check to ensure the metric movements align with the hypothesis.

* **Causal Path**: If the Success Metric (e.g., Conversion) improved, did the Diagnostic Metric (e.g., Clicks) also move in a way that explains it?
* **Contradiction Check**: If Conversion rose but "Time Spent" or "Search Success" crashed, investigate if the lift is due to a bug, dark patterns, or a shallow proxy.

### Step 12: Produce a Decision-Oriented Readout

The final output should include:

- experiment status label;
- trustworthiness assessment;
- metric hierarchy;
- effect summary;
- guardrail summary;
- segment summary;
- long-term risk;
- recommendation;
- missing evidence;
- next steps.

## 12.1 Agent Execution Protocol

The agent should execute A/B analysis in three phases.

### Phase 1: Parse and Validate Inputs

The agent must extract:

- experiment goal;
- treatment and control;
- randomization unit;
- exposure definition;
- analysis population;
- metric hierarchy;
- sample size and duration;
- validity check results;
- segment plan;
- guardrail thresholds.

If required fields are missing, the agent should continue with a provisional readout but label missing evidence explicitly.

### Phase 2: Run Decision Gates

The agent should apply gates in this order:

1. Validity gate:
   - fail → `do_not_trust_result`
2. Design appropriateness gate:
   - randomization inappropriate or interference likely → `use_quasi_experiment`
3. Evidence strength gate:
   - underpowered or wide CI → `inconclusive`
4. Guardrail gate:
   - hard guardrail fails → `mixed_tradeoff`
5. Segment gate:
   - strategic segment harmed → `segment_specific`
6. Long-term risk gate:
   - delayed harm plausible → `needs_longer_readout`
7. Launch evidence gate:
   - meaningful lift + guardrails pass + no segment harm → `positive_aligned`

### Phase 3: Produce Decision Readout

The agent output must include:

- status label;
- one-sentence decision;
- validity assessment;
- metric hierarchy;
- effect estimate;
- guardrail conclusion;
- segment conclusion;
- long-term/interference conclusion;
- missing evidence;
- recommended next step.

---

## 13. Decision Matrix

| Evidence Pattern | Experiment Status | Recommended Action |
|---|---|---|
| SRM, assignment bug, logging failure, or exposure mismatch | `do_not_trust_result` | Diagnose and rerun or repair |
| Valid test, decision metric meaningfully improves, guardrails pass, no segment harm | `positive_aligned` | Launch or use launch decision playbook |
| Valid test, success metric improves but guardrail fails | `mixed_tradeoff` | Do not launch broadly; investigate or redesign |
| Valid test, diagnostic metric improves but decision metric flat | `inconclusive` or `mixed_tradeoff` | Do not launch on diagnostic lift alone |
| Valid test, average positive but key segment harmed | `segment_specific` | Targeted rollout or further testing |
| Valid test, confidence interval includes meaningful upside and downside | `inconclusive` | Extend, rerun, or improve power |
| Valid short-term lift but long-term risk unclear | `needs_longer_readout` | Holdout, delayed readout, phased rollout |
| Marketplace/network interference likely | `use_quasi_experiment` or `needs_longer_readout` | Use cluster, geo, switchback, or quasi-experiment |
| Observational result interpreted causally | `use_quasi_experiment` | Do not claim causal effect without assumptions |
| Low-risk reversible test with small but meaningful positive lift and stable guardrails | `positive_aligned` | Launch with monitoring may be enough |
| High-risk irreversible change with moderate positive lift and unclear guardrails | `needs_longer_readout` or `mixed_tradeoff` | Conservative rollout or no launch |

---

## 14. Data Audit Queries the Agent Should Try to Run

The exact SQL depends on schema, but the agent should look for these checks.

### 14.1 Assignment Counts

```sql
select
  variant,
  count(distinct randomization_unit_id) as assigned_units
from experiment_assignment
where experiment_id = '{experiment_id}'
group by 1;
```

### 14.2 Exposure Counts

```sql
select
  variant,
  count(distinct randomization_unit_id) as exposed_units
from experiment_exposure
where experiment_id = '{experiment_id}'
group by 1;
```

### 14.3 Assigned-to-Exposed Drop-Off

```sql
select
  a.variant,
  count(distinct a.randomization_unit_id) as assigned_units,
  count(distinct e.randomization_unit_id) as exposed_units,
  count(distinct e.randomization_unit_id) * 1.0
    / nullif(count(distinct a.randomization_unit_id), 0) as exposure_rate
from experiment_assignment a
left join experiment_exposure e
  on a.randomization_unit_id = e.randomization_unit_id
 and a.experiment_id = e.experiment_id
where a.experiment_id = '{experiment_id}'
group by 1;
```

### 14.4 Duplicate Assignment

```sql
select
  randomization_unit_id,
  count(distinct variant) as variant_count
from experiment_assignment
where experiment_id = '{experiment_id}'
group by 1
having count(distinct variant) > 1;
```

### 14.5 Pre-Treatment Balance

```sql
select
  variant,
  avg(pre_period_activity) as avg_pre_period_activity,
  avg(account_age_days) as avg_account_age_days,
  avg(case when platform = 'ios' then 1 else 0 end) as ios_share
from experiment_population
where experiment_id = '{experiment_id}'
group by 1;
```

### 14.6 Metric Readout

```sql
select
  variant,
  count(distinct user_id) as users,
  avg(metric_value) as mean_metric,
  stddev(metric_value) as sd_metric
from user_level_metrics
where experiment_id = '{experiment_id}'
  and metric_name = '{metric_name}'
group by 1;
```

### 14.7 Segment Readout

```sql
select
  segment_name,
  segment_value,
  variant,
  count(distinct user_id) as users,
  avg(metric_value) as mean_metric
from user_level_metrics
where experiment_id = '{experiment_id}'
  and metric_name = '{metric_name}'
group by 1, 2, 3;
```

The agent should not invent results if data is unavailable. It should state which queries or checks are needed.

---

## 15. Common Analysis Pitfalls

### 15.1 Reading Lift Before Validity

Bad:

> Treatment improved conversion by 3%, but SRM exists. Launch carefully.

Better:

> Do not trust the result. Diagnose SRM before interpreting the conversion lift.

### 15.2 Treating P-Value as the Decision

Bad:

> p < 0.05, so the test won.

Better:

> The effect is statistically significant, but the lift is smaller than the practical threshold and guardrail risk remains.

### 15.3 Optimizing Diagnostic Metrics

Bad:

> CTR increased, so the ranking model improved.

Better:

> CTR is diagnostic. Check retention, satisfaction, hides, reports, content quality, and long-term engagement.

### 15.4 Ignoring Guardrail Power

Bad:

> Retention did not significantly decline, so retention is safe.

Better:

> The test may be underpowered for retention. The confidence interval still includes material downside.

### 15.5 Post-Hoc Metric Switching

Bad:

> The primary metric was flat, but another metric improved, so the test succeeded.

Better:

> Treat the new metric as exploratory and run a follow-up test if it represents a better hypothesis.

### 15.6 Segment Overfitting

Bad:

> One small subgroup improved, so launch there.

Better:

> Check sample size, multiple testing, strategic relevance, and replication.

### 15.7 Ignoring Reversibility

Bad:

> Apply the same evidence threshold to a button copy change and a pricing policy change.

Better:

> Higher-risk and less reversible decisions require stronger evidence and stricter guardrails.

### 15.8 Confusing Observational Evidence with Experiment Evidence

Bad:

> Users exposed to the feature retained better, so the feature caused retention.

Better:

> Exposure may be endogenous. Use randomized assignment, DiD, regression discontinuity, synthetic control, or another causal design.

### 15.9 Treating Short-Term Engagement as Durable Value

Bad:

> Watch time increased, so the product improved.

Better:

> Check whether watch time is qualified, retention is stable, satisfaction is stable, and content quality is not harmed.

### 15.10 Ignoring Interference

Bad:

> Randomize sellers individually and assume buyer outcomes are independent.

Better:

> Marketplaces may violate no-interference assumptions. Consider cluster or geo randomization.

---

## 16. Agent Output Template: A/B Test Readout

Use this structure when answering an A/B test interpretation question.

```text
Experiment status:
[ready_to_read / do_not_trust_result / inconclusive / positive_aligned / negative_aligned / mixed_tradeoff / segment_specific / needs_longer_readout / use_quasi_experiment]

Decision problem:
[What decision is the test meant to inform?]

Product context:
- Surface:
- Treatment:
- Target population:
- Risk tier:
- Reversibility:

Experiment design:
- Randomization unit:
- Exposure definition:
- Analysis unit:
- Duration:
- Sample size:
- Stopping rule:

Metric hierarchy:
- Decision metric:
- Success metrics:
- Guardrail metrics:
- Diagnostic metrics:
- Invariant metrics:

Validity first:
- SRM:
- Assignment consistency:
- Exposure consistency:
- Logging completeness:
- Contamination:
- Post-treatment filtering:
- Invariant balance:
- Peeking / early stopping:

Effect readout:
- Decision metric effect:
- Practical magnitude:
- Confidence interval:
- Statistical evidence:
- Guardrail non-inferiority:
- Segment effects:
- Long-term / ecosystem risk:

Recommendation:
[What should be done next?]

Missing evidence:
- [Evidence 1]
- [Evidence 2]
- [Evidence 3]

Next steps:
- [Analysis or experiment step]
- [Monitoring step]
- [Decision or rollback threshold]
```

---

## 17. Agent Output Template: Experiment Design Proposal

Use this when the user asks how to design an A/B test.

```text
Experiment objective:
[Product decision and hypothesis.]

Recommended design:
[User-level A/B / session-level A/B / cluster randomized / geo / switchback / quasi-experiment.]

Why this design:
[Why the unit and design match the product mechanism.]

Population:
[Eligibility and exclusions.]

Variants:
- Control:
- Treatment:

Randomization:
- Unit:
- Assignment:
- Persistence:

Exposure:
[What counts as exposure.]

Metrics:
- Decision metric:
- Success metrics:
- Guardrails:
- Diagnostics:
- Invariants:

Power and duration:
- MDE:
- Planned duration:
- Required sample size:
- Readout windows:

Validity checks:
- SRM:
- Logging:
- Exposure:
- Balance:
- Contamination:
- Peeking:

Segment plan:
[Pre-specified and strategic segments.]

Long-term risk:
[Holdout or delayed readout if needed.]

Decision rule:
[Launch, partial rollout, investigate, or no launch criteria.]
```

---

## 18. Evaluation Criteria for Agent Answers

A high-quality A/B testing answer should:

- clarify the causal question;
- identify the product decision;
- classify the experiment status;
- define metric hierarchy;
- check validity before lift;
- explicitly mention SRM when relevant;
- separate assignment, exposure, and analysis populations;
- distinguish success metrics from guardrails and diagnostics;
- report both statistical uncertainty and practical magnitude;
- use non-inferiority logic for guardrails;
- scan segments without overfitting noise;
- consider long-term and ecosystem risks;
- recognize interference when applicable;
- recommend quasi-experimental design when randomization is unavailable;
- provide concrete next steps;
- avoid overclaiming when data is incomplete.

Penalize an answer if it:

- recommends launch based only on p-value;
- treats an invalid experiment as causal;
- ignores SRM;
- ignores guardrail deterioration;
- ignores strategic segment harm;
- treats CTR, clicks, impressions, or time spent as sufficient by themselves;
- ignores experiment duration and peeking;
- ignores randomization or exposure unit;
- fails to distinguish diagnostics from decision metrics;
- gives generic advice without a status label;
- asks many clarifying questions without giving a provisional framework;
- cherry-picks favorable metrics after reading results;
- ignores interference in marketplaces, social products, ads, or recommendation systems.

A strong answer should feel like a senior experimentation scientist writing a concise product decision review.

---

## 19. Minimum Required Evidence for an Experiment Readout

An experiment readout should include:

### 19.1 Recommendation Summary

- experiment status label;
- provisional launch implication;
- confidence level;
- key reason.

### 19.2 Experiment Design

- hypothesis;
- control and treatment;
- target population;
- randomization unit;
- exposure definition;
- analysis unit;
- sample size;
- duration;
- stopping rule.

### 19.3 Validity Checks

- SRM;
- assignment consistency;
- exposure consistency;
- logging completeness;
- invariant balance;
- contamination;
- missingness;
- duplicates;
- bot/spam imbalance;
- pipeline changes;
- instrumentation changes;
- peeking or early stopping.

### 19.4 Metric Results

- decision metric;
- success metrics;
- guardrails;
- diagnostics;
- practical effect size;
- confidence intervals;
- non-inferiority tests for guardrails.

### 19.5 Segment Results

- pre-specified segments;
- strategic segments;
- sample sizes;
- effect direction and magnitude;
- whether segment findings are confirmatory or exploratory.

### 19.6 Risk Assessment

- reversibility;
- operational risk;
- user trust risk;
- business risk;
- marketplace risk;
- long-term risk;
- ecosystem risk.

### 19.7 Next Steps

- launch, monitor, partial rollout, redesign, rerun, or quasi-experiment;
- monitoring metrics;
- rollback thresholds;
- owner and timeline if available.

---

## 20. Final Rule

The agent should optimize for responsible causal decision quality.

When validity fails, do not trust the result.

When evidence is weak, say what is missing.

When metrics conflict, use metric hierarchy and guardrail tolerance.

When averages hide harm, protect strategic segments.

When short-term lift may create long-term harm, require holdout or delayed readout.

When interference is likely, do not rely blindly on individual-level A/B testing.

When the result is positive, meaningful, valid, safe, and aligned with durable value, treat it as actionable evidence.

The best A/B testing answer is not the most optimistic answer. It is the answer that makes the causal question, evidence, uncertainty, risk, and next action explicit.

---

## References and Source Notes

This playbook synthesizes public experimentation methodology and industry practice from the following sources:

1. Ron Kohavi, Diane Tang, and Ya Xu, *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*, Cambridge University Press, 2020.  
   https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/introductory-topics-for-everyone/9C9CAEDA5A192FF74D5EBACEB44886F0

2. Microsoft Experimentation Platform, “Patterns of Trustworthy Experimentation: Pre-Experiment Stage.”  
   https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/

3. Microsoft Experimentation Platform, “Patterns of Trustworthy Experimentation: Post-Experiment Stage.”  
   https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-post-experiment-stage/

4. Microsoft Research, “Diagnosing Sample Ratio Mismatch in A/B Testing.”  
   https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/

5. Airbnb Engineering, “Experiments at Airbnb.”  
   https://medium.com/airbnb-engineering/experiments-at-airbnb-e2db3abf39e7

6. Airbnb Engineering, “Experiment Reporting Framework.”  
   https://medium.com/airbnb-engineering/experiment-reporting-framework-4e3fcd29e6c0

7. Iavor Bojinov and Somit Gupta, “Online Experimentation: Benefits, Operational and Methodological Challenges, and Scaling Guide,” *Harvard Data Science Review*, 2022.  
   https://hdsr.mitpress.mit.edu/pub/aj31wj81

8. Simons Institute / Berkeley, “Temporal Interference and the Design of Switchback Experiments: A Markov Chain Approach.”  
   https://simons.berkeley.edu/talks/temporal-interference-design-switchback-experiments-markov-chain-approach

9. David Holtz et al., “Reducing Interference Bias in Online Marketplace Experiments Using Cluster Randomization: Evidence from a Pricing Meta-experiment on Airbnb,” *Management Science*.  
   https://pubsonline.informs.org/doi/10.1287/mnsc.2020.01157
