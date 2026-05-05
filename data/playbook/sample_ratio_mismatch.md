# Sample Ratio Mismatch Playbook

This playbook defines how an Agent should detect, diagnose, interpret, and act on Sample Ratio Mismatch (SRM) in online experiments.

It is designed for an evaluation-driven Agentic RAG system. The goal is not to make the Agent mechanically compute a chi-square test. The goal is to make the Agent behave like a senior data scientist who treats SRM as an evidence-validity failure, localizes the likely root cause, and prevents invalid experiment results from entering launch decisions.

SRM is not a metric result. SRM is a warning that the experiment evidence chain may be broken.

The governing principle is:

> **No trusted sample ratio, no trusted experiment, no responsible decision.**

---

## Quick Retrieval Summary

Use this playbook when the user asks about:

- sample ratio mismatch;
- SRM alerts;
- treatment/control imbalance;
- unequal traffic split;
- suspicious experiment population counts;
- missing users;
- exposure imbalance;
- triggered population imbalance;
- metric-level imbalance;
- whether an experiment with SRM can be trusted;
- whether a positive lift can still support launch despite SRM;
- how to diagnose SRM root causes;
- whether to rerun, repair, restrict, or discard an experiment result.

This playbook is especially relevant when:

- the observed traffic allocation differs from the configured allocation;
- the expected split is 50/50, 90/10, 1/1/1, or another fixed assignment ratio;
- an experiment result looks strong but the sample sizes are imbalanced;
- assignment counts are balanced but exposure or metric counts are imbalanced;
- a triggered analysis shows imbalance;
- one platform, app version, country, browser, device type, or traffic source shows strong imbalance;
- a treatment changes eligibility, exposure probability, logging probability, or trigger probability;
- users can appear in multiple variants;
- experiment ramp, feature flag, or allocation changed during the test;
- telemetry, identity, joins, filters, or metric denominators may be wrong.

Default reasoning order:

1. Identify the expected allocation ratio.
2. Measure observed counts at the right population level.
3. Run the SRM detection test.
4. Determine where SRM appears: assignment, exposure, trigger, metric, segment, or pipeline.
5. Classify severity.
6. Diagnose the likely root cause.
7. Decide which metrics, if any, remain reliable.
8. Decide whether causal analysis can proceed.
9. Recommend repair, rerun, restricted analysis, or `do_not_trust_result`.
10. Preserve an audit trail.

---

## 1. Core Principle

SRM is an evidence-validity problem, not a business-metric movement.

An A/B test relies on the assumption that treatment and control groups are comparable except for the treatment. When the observed allocation differs from the configured allocation, the Agent must assume that one of the following may have happened:

- randomization failed;
- assignment was not logged correctly;
- one variant failed to load;
- users were dropped differently by variant;
- the treatment changed exposure or trigger probability;
- a join or filter removed one variant disproportionately;
- identity resolution changed the denominator;
- telemetry or pipeline logic changed during the experiment;
- users self-selected into one variant;
- traffic allocation was changed incorrectly.

The Agent must not treat the measured lift as causal evidence until the SRM root cause is understood.

Bad reasoning:

> Treatment conversion increased by 3%, but SRM is detected. Launch with monitoring.

Good reasoning:

> Do not trust the result. SRM means the treatment/control populations may not be comparable. The measured 3% lift should not be interpreted causally until the SRM is diagnosed and the experiment is repaired, rerun, or reanalyzed using a valid population.

---

## 2. What SRM Means

Sample Ratio Mismatch occurs when the observed number of experimental units in each variant differs statistically from the expected assignment ratio.

Examples:

- Expected 50/50 split, observed 55/45.
- Expected 90/10 split, observed 87/13.
- Expected equal split across three arms, observed 30/40/30.
- Assignment counts are balanced, but exposure counts are 48/52.
- Assignment counts are balanced globally, but mobile traffic is 60/40.
- Triggered analysis is 70/30 because the treatment increases trigger probability.

SRM is usually detected using a goodness-of-fit test such as Pearson's chi-square test.

Important distinction:

- **SRM detection** tells the Agent that the observed ratio is unlikely under the configured assignment rule.
- **SRM diagnosis** tells the Agent why the ratio is wrong and whether any part of the analysis can still be trusted.

Detection without diagnosis is not enough for a responsible launch decision.

---

## 3. SRM Detection Contract

The Agent must verify all of the following before declaring SRM status.

### 3.1 Required Inputs

The Agent needs:

- expected allocation ratio;
- observed counts by variant;
- experimental unit;
- randomization unit;
- analysis population;
- experiment start and end time;
- ramp history;
- active variants;
- assignment table or event;
- exposure table or event when applicable;
- metric observation table when applicable;
- segment dimensions used for diagnosis.

If expected allocation is unknown, the Agent must not invent a 50/50 split. It should mark the result as `experiment_unreliable` or request/derive allocation from experiment configuration.

### 3.2 Detection Test

For variants `i = 1, ..., k`:

- observed count: `O_i`
- expected allocation probability: `p_i`
- total count: `N = sum(O_i)`
- expected count: `E_i = N * p_i`

Chi-square statistic:

```text
chi_square = sum((observed_i - expected_i)^2 / expected_i)
df = number_of_active_variants - 1
p_value = P(ChiSquare(df) >= chi_square)
```

Agent Action:

- Use the platform-configured SRM threshold when available.
- If no platform threshold is provided, use a conservative threshold such as `alpha = 0.001` or stricter.
- Do not tune the threshold after seeing metric results.
- Do not ignore SRM because business metrics are statistically significant.

> **Senior Note on Scale:** In massive experiments (N > 100M), a ratio of 50.01/49.99 might trigger a p-value $< 0.001$. While statistically significant, this "micro-SRM" may be caused by negligible upstream hash-collision noise rather than a systemic bias. The Agent should evaluate the **imbalance magnitude** alongside the p-value before declaring the entire experiment "unreliable."

### 3.3 Threshold Guidance

The threshold is not a universal law. It is a platform policy choice.

Recommended behavior:

| Context | Suggested Threshold Behavior |
|---|---|
| Mature experimentation platform | Use platform-configured SRM alpha |
| No platform threshold | Use conservative alpha such as 0.001 |
| High-volume experiments | Use stricter threshold and stronger diagnosis |
| Continuous monitoring / repeated checks | Use conservative threshold because repeated peeking increases false positives |
| High-risk launch decision | Treat any credible SRM as blocking until diagnosed |
| Small experiment | Do not overreact to tiny absolute differences; still compute test and inspect counts |

The Agent should report both p-value and absolute imbalance. A tiny ratio deviation can be statistically significant at very large scale, while a large-looking deviation may be statistically plausible at small sample size.

### 3.4 SRM Multiple Testing Caution

A senior data scientist knows that checking SRM across dozens of segments (e.g., every country, every browser version) increases the probability of finding a "false positive" SRM by chance.

- **The Problem:** If you check 20 independent segments with $\alpha = 0.05$, there is a 64% chance of seeing at least one SRM alert even if the randomization is perfect.
- **Agent Action:** - Do not panic over a single localized SRM alert if global SRM is clean, unless the p-value is extremely low (e.g., $< 10^{-5}$) or the segment is a primary target.
    - Use Bonferroni correction or Benjamini-Hochberg procedure when performing mass-segment SRM audits.
    - Prioritize segments with high volume; small-sample segments are prone to noise-driven SRM.

---

## 4. Where SRM Must Be Checked

A strong Agent does not check SRM only once.

SRM can appear at different points in the experiment evidence chain. Each level has a different interpretation.

| Level | Question | Why It Matters |
|---|---|---|
| Assignment-level SRM | Were users assigned according to the configured ratio? | Tests randomization, allocation, identity, and assignment logging |
| Exposure-level SRM | Did assigned users actually receive exposure at expected rates? | Detects load failure, redirect, treatment-specific exposure loss, exposure logging bugs |
| Triggered-population SRM | Did the triggered analysis population remain balanced? | Detects treatment-induced triggering or biased analysis population |
| Metric-level SRM | Are users/events contributing to a metric balanced? | Detects metric-specific logging, joins, missingness, or denominators |
| Segment-level SRM | Is imbalance localized to browser, app version, country, platform, cohort, etc.? | Helps localize root cause and determine whether restricted analysis is possible |
| Time-slice SRM | Does imbalance appear only after a ramp, deploy, outage, or pipeline change? | Detects temporal changes and release interactions |
| Identity-level SRM | Are users appearing in multiple variants or being re-identified? | Detects unstable IDs, cross-device issues, cookie resets, or mixed assignments |

Agent Action:

- Always start with assignment-level SRM.
- If assignment is clean but exposure is not, investigate execution or exposure logging.
- If assignment and exposure are clean but triggered population is not, investigate trigger symmetry and post-treatment selection.
- If only one metric shows imbalance, classify that metric as unreliable rather than discarding the entire experiment immediately.
- If SRM is localized to a non-strategic segment and the root cause is understood, restricted analysis may be possible.
- If SRM affects the main decision population, do not trust the experiment result.

---

## 5. Severity Labels

The Agent must assign exactly one primary SRM severity label.

Allowed labels:

- `clean`
- `minor_warning`
- `metric_unreliable`
- `experiment_unreliable`
- `pipeline_blocker`

### 5.1 `clean`

Use when:

- assignment-level SRM passes;
- exposure-level SRM passes when exposure is relevant;
- triggered population is valid or not used;
- metric-level population checks pass for decision metrics;
- no critical segment-level imbalance is detected;
- no mixed-assignment or identity instability is material.

Causal analysis may proceed.

### 5.2 `minor_warning`

Use when:

- a small imbalance appears in a non-decision segment;
- the imbalance is not in the assignment, exposure, trigger, or decision-metric population;
- root cause is understood and not expected to bias the main result;
- decision metrics remain reliable.

Causal analysis may proceed with caveats.

Agent must explicitly state why the warning does not invalidate the decision.

### 5.3 `metric_unreliable`

Use when:

- SRM or imbalance affects one or more specific metrics;
- the overall assignment is clean;
- the metric denominator, join, or event logging is variant-biased;
- the affected metric should not be used in the launch decision;
- other metrics may remain reliable.

Examples:

- refund events missing only for treatment users;
- checkout event duplicated only in control;
- one diagnostic click metric has treatment-specific logging;
- support-ticket metric is immature or filtered differently.

Causal analysis may proceed only for unaffected metrics.

### 5.4 `experiment_unreliable`

Use when:

- assignment-level SRM is detected;
- exposure-level SRM invalidates the treatment/control comparison;
- triggered population is treatment-induced and used as the primary analysis population;
- post-treatment filtering creates imbalance;
- users can self-select into variants;
- identity instability or mixed assignments is material;
- SRM root cause is unknown and decision metrics depend on the affected population.

The experiment result should not be used as causal launch evidence.

### 5.5 `pipeline_blocker`

Use when:

- assignment, exposure, or metric data is missing or corrupted;
- schema changed mid-experiment;
- pipeline backfill changed counts inconsistently;
- joins cannot be trusted;
- event timestamps or ingestion windows are broken;
- experiment configuration snapshot is missing;
- analysis cannot be reproduced.

The Agent should stop causal interpretation and recommend data repair, backfill, or rerun.

---

## 6. Root Cause Taxonomy

SRM can originate at multiple stages of the experiment lifecycle.

The Agent should localize the root cause by stage.

### 6.1 Configuration and Design Stage

Possible causes:

- wrong expected allocation ratio;
- experiment configured as 50/50 but launched as 90/10;
- uneven ramp across variants;
- mid-experiment traffic allocation change;
- overlapping experiments in the same layer;
- mutual exclusion layer misconfigured;
- eligibility rule differs by variant;
- experiment start time differs across variants;
- holdout or traffic split not included in expected ratio;
- inactive or paused variant not excluded from active allocation.

Agent must check:

- configured allocation;
- ramp schedule;
- feature flag history;
- active variants;
- experiment layer;
- eligibility rules;
- holdout rules;
- experiment start/end timestamps.

### 6.2 Assignment Stage

Possible causes:

- bucketing bug;
- wrong hash key;
- unstable randomization unit;
- user ID or device ID instability;
- logged-out to logged-in identity change;
- cross-device duplication;
- cookie deletion or privacy setting effects;
- re-randomization;
- carryover from prior experiment;
- assignment event not emitted consistently;
- assignment service outage.

Agent must check:

- randomization unit;
- deterministic assignment behavior;
- assignment log completeness;
- duplicate assignments;
- mixed assignments;
- user/device/session mapping;
- assignment service version.

### 6.2.1 Upstream Selection Bias vs. Downstream SRM
A top scientist distinguishes between:
- **Assignment SRM:** The bucketing logic itself is broken (Internal Validity).
- **Selection Bias:** The experiment population doesn't represent the target population (External Validity), often caused by "Pre-assignment filtering" that is unintentionally variant-aware (e.g., a shared cache state from a previous experiment).

### 6.3 Execution and Exposure Stage

Possible causes:

- one variant fails to load;
- treatment redirects users;
- treatment changes page load time;
- treatment causes crash or render failure;
- treatment changes eligibility after assignment;
- exposure event emitted only after successful render;
- exposure logging differs by variant;
- users leave before exposure is logged;
- control and treatment have different code paths for telemetry;
- treatment changes engagement enough to trigger bot/spam filters.

Agent must check:

- render success;
- variant load failure;
- latency;
- crash rate;
- exposure event symmetry;
- client/server logging;
- redirect/drop-off;
- eligibility after assignment;
- bot/spam filtering by variant.

### 6.4 Logging and Pipeline Stage

Possible causes:

- missing assignment events;
- missing exposure events;
- duplicated assignment or exposure events;
- duplicated outcome events;
- variant-specific telemetry loss;
- event schema change;
- event name changed mid-experiment;
- failed extraction;
- delayed ingestion;
- pipeline backfill;
- incorrect timezone;
- incorrect date window;
- client and server logs disagree;
- privacy/consent filtering affects one variant.

Agent must check:

- event completeness;
- duplicate rates;
- missingness by variant;
- late-arriving events;
- schema versions;
- ETL run history;
- pipeline backfills;
- event timestamp vs ingestion timestamp;
- privacy/consent filters.

### 6.5 Analysis Stage

Possible causes:

- post-treatment filtering;
- biased triggered analysis;
- wrong denominator;
- incorrect joins;
- one-to-many joins;
- filtering on a variable affected by treatment;
- excluding bots/spam after treatment changes behavior;
- including only converters;
- segment membership affected by treatment;
- metric observation window differs by variant;
- using exposed-only analysis when exposure is treatment-induced.

Agent must check:

- analysis population;
- joins and join keys;
- filters;
- deduplication rules;
- trigger definition;
- whether trigger is pre-treatment or post-treatment;
- metric denominator;
- segment stability;
- metric windows.

---

## 7. Differential Diagnosis Workflow

When SRM is detected, the Agent should follow this workflow.

### Step 1: Confirm Expected Allocation

Agent must verify:

- expected split;
- active variants;
- holdout group;
- ramp history;
- traffic allocation changes;
- experiment start/end time.

If expected allocation cannot be confirmed, assign `experiment_unreliable`.

### Step 2: Recompute SRM on Assignment Population

Agent must compute observed counts by variant using the assignment event or assignment table.

If assignment-level SRM is present:

- suspect configuration, randomization, identity, or assignment logging;
- do not interpret business metrics;
- assign `experiment_unreliable` or `pipeline_blocker`.

### Step 3: Check Exposure Population

If assignment-level SRM is clean, compare exposure counts.

If exposure-level SRM appears:

- suspect load failure, rendering, redirects, exposure logging, latency, or eligibility changes;
- determine whether exposure is part of the causal estimand;
- do not use exposed-only analysis without bias assessment.

### Step 4: Check Triggered Population

If a triggered analysis is used, verify trigger validity.

Trigger is valid only if:

- trigger condition is defined before treatment can affect it; or
- trigger is observable symmetrically in treatment and control; and
- treatment cannot materially change trigger probability.

If trigger is treatment-induced, assign `experiment_unreliable` for triggered readout and use ITT or redesign.

### Step 5: Check Metric-Level Population

For each decision metric:

- count users/events contributing to metric by variant;
- check missingness by variant;
- check duplicate rates by variant;
- check join success by variant;
- check metric window maturity.

If only one metric fails, use `metric_unreliable`.

### Step 6: Slice by Static Segments

Analyze SRM by stable, pre-treatment dimensions:

- platform;
- browser;
- app version;
- geography;
- device type;
- logged-in status at assignment;
- acquisition channel;
- pre-period activity;
- experiment entry date;
- traffic source.

Avoid dynamic segments affected by treatment, such as post-treatment active days, conversion status, engagement level, or exposure count.

### Step 7: Inspect Time Series

Check whether SRM begins after:

- ramp change;
- code deployment;
- feature flag update;
- pipeline backfill;
- logging schema change;
- outage;
- bot/spam filter update;
- platform release.

If SRM is localized to a time window, restricted reanalysis may be possible only if the remaining window is valid and sufficiently powered.

### Step 8: Decide Salvageability

Possible outcomes:

- discard result and rerun;
- repair data and recompute scorecard;
- restrict to unaffected segment;
- restrict to unaffected metrics;
- use ITT instead of triggered/exposed analysis;
- use quasi-experimental repair only if randomized evidence is unsalvageable and assumptions are stated.

Do not salvage an experiment merely because the result is desirable.

### 7.1 Advanced Diagnostic: Automated Segment Discovery

Instead of manually checking static segments, a top-tier Agent uses machine learning logic to localize SRM.

- **SRM Decision Trees:** Train a simple decision tree where the target is the `variant_assignment` (e.g., 0 for Control, 1 for Treatment) and the features are user attributes.
- **Interpretation:** If the tree can easily "predict" which variant a user belongs to based on attributes (e.g., "If AppVersion < 5.0, then 80% chance of Treatment"), you have found the exact segment where the randomization or logging failed.
- **Benefit:** This moves from "guessing" segments to "calculating" the source of bias.

---

## 8. ITT, Exposure, and Triggered Analysis Rules

SRM diagnosis depends on the analysis population.

### 8.1 Intent-to-Treat Analysis

ITT includes all assigned units.

Use ITT when:

- treatment exposure can be imperfect;
- exposure is affected by treatment;
- trigger is post-treatment;
- assignment is trustworthy;
- the decision is about launching the assignment policy itself.

Strength:

- preserves randomization.

Weakness:

- may dilute effects if many assigned units are never exposed.

### 8.2 Exposed-User Analysis

Exposed-user analysis includes users who were exposed to the experiment.

Use only when:

- exposure is logged symmetrically;
- exposure opportunity exists equally across variants;
- exposure is not caused by treatment-specific behavior;
- non-exposed users are not systematically different by variant.

Risk:

- if treatment affects exposure probability, exposed-only analysis is post-treatment selection.

### 8.3 Triggered Analysis

Triggered analysis includes users who meet a trigger condition.

Valid triggered analysis requires:

- trigger condition is pre-treatment or treatment-invariant;
- trigger can be observed equally in control and treatment;
- treatment does not change probability of entering trigger population.

Invalid triggered analysis examples:

- Treatment increases search activity, and analysis includes only users who searched.
- Treatment changes page load speed, and analysis includes only users with successful render.
- Treatment changes notification opens, and analysis includes only openers.
- Treatment changes checkout entry, and analysis includes only checkout entrants.

Agent Action:

- If trigger is treatment-induced, do not use triggered readout as causal evidence.
- Prefer ITT or redesign the trigger.
- If triggered analysis is used, report triggered-population SRM separately.

### 8.4 Per-Protocol Analysis

Per-protocol analysis includes users who complied with treatment.

This is usually not appropriate for product launch decisions unless compliance is pre-treatment or randomized.

Risk:

- compliance may be caused by treatment or user preference.

Agent should treat per-protocol results as diagnostic, not primary causal evidence.

---

## 9. SRM Decision Matrix

| Evidence Pattern | Severity | Agent Action |
|---|---|---|
| Assignment-level SRM | `experiment_unreliable` | Do not interpret lift; diagnose allocation, bucketing, identity, assignment logging |
| Expected allocation unknown | `experiment_unreliable` | Recover configuration snapshot before analysis |
| Assignment clean, exposure SRM detected | `experiment_unreliable` or `metric_unreliable` | Check load failure, redirects, exposure logging, latency, eligibility |
| Assignment/exposure clean, decision metric population imbalanced | `metric_unreliable` | Exclude or repair affected metric |
| Triggered SRM and trigger may be affected by treatment | `experiment_unreliable` | Use ITT or redesign trigger |
| Triggered SRM but trigger is pre-treatment and root cause localized | `minor_warning` or `metric_unreliable` | Document root cause and restrict analysis if valid |
| Segment-level SRM in important segment | `experiment_unreliable` or `investigate_further` | Diagnose segment-specific logging or assignment issue |
| SRM localized to non-decision segment with known benign cause | `minor_warning` | Proceed with caveat if main decision population is clean |
| Mixed assignments are material | `experiment_unreliable` | Remove invalid users only if removal is variant-neutral; otherwise rerun |
| Duplicate events in one variant | `metric_unreliable` or `pipeline_blocker` | Repair dedup logic and recompute |
| Schema changed mid-experiment | `pipeline_blocker` | Repair/backfill or rerun |
| Pipeline backfill changes counts inconsistently | `pipeline_blocker` | Freeze data version and recompute |
| Bot filter removes treatment users disproportionately | `experiment_unreliable` | Diagnose whether filter is treatment-induced; repair or rerun |
| SRM disappears after documented data repair | `clean` after repair | Recompute all results and include audit note |
| SRM remains unexplained | `experiment_unreliable` | Do not use experiment for launch decision |

---

## 10. Context-Specific SRM Handling

### 10.1 UI or Client-Side Experiments

Common SRM causes:

- treatment fails to render;
- JavaScript error prevents logging;
- client event fires only in one variant;
- slower treatment causes users to leave before exposure logging;
- browser or app-version incompatibility.

Agent must check:

- render success;
- client error rate;
- exposure event timing;
- browser/app-version segment SRM;
- event-send success.

### 10.2 Search, Feed, and Recommendation Experiments

Common SRM causes:

- treatment changes engagement and therefore trigger probability;
- triggered analysis conditions are post-treatment;
- bot/spam filters remove high-engagement users;
- treatment changes exposure volume;
- ranking changes create segment-specific exposure.

Agent must check:

- ITT vs triggered population;
- pre-treatment trigger validity;
- exposure opportunity;
- bot/spam filter by variant;
- segment SRM by platform and traffic source.

### 10.3 Ads Experiments

Common SRM causes:

- ad render failure;
- auction eligibility changes;
- privacy/consent filtering;
- advertiser/publisher eligibility drift;
- delayed conversion attribution;
- treatment changes ad load and exposure counts.

Agent must check:

- assignment vs impression-level counts;
- auction participation;
- exposure logging;
- conversion attribution window;
- advertiser/placement/device segment SRM.

If ads marketplace interference is material, also use `ads_experiments.md`.

### 10.4 Marketplace Experiments

Common SRM causes:

- treatment changes inventory availability;
- one side of the marketplace receives different exposure opportunities;
- supply-constrained treatments crowd out control units;
- local market allocation differs by geography or time;
- market-level experiment units are miscounted.

Agent must check:

- buyer-side and seller-side counts;
- market-level units;
- geography/time SRM;
- shared inventory interference;
- local-market balance.

If interference is likely, also use `marketplace_metrics.md`.

### 10.5 Mobile App Experiments

Common SRM causes:

- app version rollout imbalance;
- delayed upgrade adoption;
- OS-specific logging bug;
- crash before exposure event;
- offline events arrive late;
- privacy/consent differences.

Agent must check:

- app version;
- OS version;
- crash rate;
- offline ingestion delay;
- event timestamp vs ingestion timestamp;
- platform-specific SRM.

### 10.6 Long-Running or Ramped Experiments

Common SRM causes:

- allocation changes over time;
- variant starts late;
- ramp is uneven;
- assignment service changes;
- feature flag changes;
- data pipeline changes mid-test.

Agent must check:

- daily SRM;
- cumulative SRM;
- ramp logs;
- config snapshots;
- deployment timeline;
- pre/post-change reanalysis.

---

## 11. SRM Debugging Checklist

### 11.1 Configuration Checklist

Agent must check:

- expected allocation ratio;
- active variant list;
- holdout allocation;
- ramp history;
- start/end time;
- experiment layer;
- mutually exclusive experiments;
- feature flag status;
- eligibility rules;
- allocation changes during test.

### 11.2 Identity Checklist

Agent must check:

- randomization unit;
- user_id stability;
- device_id stability;
- logged-in vs logged-out behavior;
- cross-device duplication;
- cookie reset;
- privacy/consent changes;
- mixed assignments;
- re-randomization.

### 11.3 Assignment Checklist

Agent must check:

- assignment count by variant;
- assignment event completeness;
- deterministic assignment;
- bucketing hash;
- assignment service errors;
- duplicate assignments;
- users assigned to multiple variants;
- carryover from prior experiments.

### 11.4 Exposure Checklist

Agent must check:

- exposure count by variant;
- exposure event symmetry;
- render success;
- treatment load failure;
- redirect/drop-off;
- latency;
- crash rate;
- eligibility after assignment;
- control/treatment code path differences.

### 11.5 Logging Checklist

Agent must check:

- missing assignment events;
- missing exposure events;
- missing outcome events;
- duplicate events;
- late-arriving events;
- schema versions;
- event name changes;
- client/server mismatch;
- ingestion failures;
- pipeline backfills;
- timezone alignment.

### 11.6 Analysis Checklist

Agent must check:

- analysis population;
- filters;
- joins;
- join keys;
- dedup rules;
- trigger definition;
- metric denominator;
- metric window;
- post-treatment variables;
- segment stability;
- bot/spam filtering.

---

## 12. Salvage and Repair Rules

Not all SRM cases require throwing away all data, but the Agent must be conservative.

### 12.1 When the Experiment Is Not Salvageable

Do not use the experiment for causal decisions when:

- assignment-level SRM remains unresolved;
- root cause is unknown;
- post-treatment filtering affects the primary analysis population;
- exposure logging is asymmetric and cannot be repaired;
- mixed assignments are material;
- pipeline or schema corruption cannot be corrected;
- affected users are likely those most impacted by treatment.

Recommendation:

- repair root cause;
- rerun experiment;
- do not use measured lift.

### 12.2 When Metric-Level Salvage May Be Possible

Metric-level restricted analysis may be possible when:

- assignment and exposure populations are clean;
- only one metric has a known logging or join issue;
- affected metric is not the sole decision metric;
- unaffected metrics have independent reliable data lineage;
- the issue is documented.

Recommendation:

- classify affected metric as `metric_unreliable`;
- exclude it from decision or repair and recompute;
- do not let one broken metric imply all other metrics are broken unless evidence supports that.

### 12.3 When Segment-Level Salvage May Be Possible

Segment-level restricted analysis may be possible when:

- SRM is localized to a known segment;
- segment is defined by pre-treatment attributes;
- segment is not strategically required for broad launch;
- unaffected segments remain balanced and sufficiently powered;
- the root cause does not plausibly affect unaffected segments.

Recommendation:

- restrict analysis only if the restriction was justified by diagnosis, not result shopping;
- label the decision as `partial_rollout` or `investigate_further`, not broad launch.

### 12.4 When Repair and Recompute Is Possible

Repair may be possible when:

- duplicate events can be deduplicated consistently;
- missing events can be backfilled from a reliable source;
- schema version can be mapped correctly;
- incorrect join can be corrected;
- bot filter can be rerun with treatment-invariant logic.

Requirements:

- document repair logic;
- recompute SRM after repair;
- recompute all results after repair;
- compare pre-repair and post-repair conclusions;
- include audit trail.

---

## 13. Prevention Rules

A top data scientist should not only diagnose SRM after the fact. The Agent should also recommend prevention.

### 13.1 Pre-Experiment Prevention

Before launch:

- validate assignment service;
- run an A/A test if platform or assignment code changed;
- freeze expected allocation;
- record configuration snapshot;
- define randomization unit;
- define exposure event;
- define analysis population;
- define trigger conditions;
- avoid treatment-affected triggers;
- document metric denominators;
- ensure assignment and exposure events are emitted symmetrically;
- test telemetry on all major platforms and app versions.

### 13.2 During-Experiment Monitoring

During the experiment:

- monitor SRM early;
- monitor daily and cumulative counts;
- alert on assignment SRM;
- alert on exposure SRM;
- alert on mixed assignments;
- monitor major platform/version segments;
- monitor event completeness and duplicate rates;
- monitor guardrails such as latency, crash rate, and render success;
- pause or auto-shutdown if severe SRM appears.

### 13.3 Post-Experiment Audit

Before analyzing effects:

- rerun SRM on frozen data;
- compare counts across assignment, exposure, trigger, and metric populations;
- check static segment SRM;
- check metric-level missingness;
- check pipeline history;
- document any warning;
- assign severity label before interpreting metrics.

---

## 14. Minimum Evidence Required for SRM Diagnosis

An SRM diagnosis should include:

### 14.1 Experiment Configuration

- experiment name;
- variants;
- expected allocation;
- randomization unit;
- assignment source;
- exposure source;
- analysis population;
- start/end time;
- ramp history;
- active variants;
- experiment layer.

### 14.2 SRM Test Result

- observed counts;
- expected counts;
- chi-square statistic;
- degrees of freedom;
- p-value;
- alpha threshold;
- pass/fail status;
- absolute imbalance;
- relative imbalance.

### 14.3 Location of Imbalance

- assignment-level;
- exposure-level;
- triggered population;
- metric-level;
- segment-level;
- time-slice-level;
- identity-level.

### 14.4 Root Cause Hypotheses

- most likely causes;
- supporting evidence;
- rejected causes;
- missing evidence.

### 14.5 Decision Impact

- reliable metrics;
- unreliable metrics;
- whether causal analysis can proceed;
- whether launch decision can use the result;
- required repair or rerun.

---

## 15. Agent Response Template

Use this structure when answering SRM-related questions.

```text
SRM Status:
[clean / minor_warning / metric_unreliable / experiment_unreliable / pipeline_blocker]

Can causal analysis proceed?
[yes / no / only for unaffected metrics or segments]

Expected allocation:
[...]

Observed allocation:
[...]

SRM test:
- Test:
- Statistic:
- Degrees of freedom:
- P-value:
- Threshold:
- Conclusion:

Where SRM appears:
- Assignment population:
- Exposure population:
- Triggered population:
- Metric population:
- Segment population:
- Time-slice population:

Root-cause diagnosis:
1. [Most likely cause]
2. [Second likely cause]
3. [Third likely cause]

Reliable evidence:
- [...]

Unreliable evidence:
- [...]

Decision impact:
[Explain whether the experiment can support launch, partial rollout, further investigation, or must be rerun.]

Recommended action:
[repair / rerun / restrict analysis / use ITT / exclude affected metric / do_not_trust_result]

Audit trail:
- assignment table:
- exposure table:
- event tables:
- date range:
- filters:
- joins:
- dedup rules:
- metric versions:
- config snapshot:
```

---

## 16. Example Reasoning Patterns

### 16.1 Positive Lift with Assignment-Level SRM

User asks:

> Treatment increased conversion by 3%, but the sample ratio is 54/46 instead of 50/50. Should we launch?

Bad answer:

> The lift is strong, so launch with monitoring.

Good answer:

> Do not trust the result. Assignment-level SRM means the treatment and control groups may not be comparable. The 3% lift should not be interpreted as causal evidence. Diagnose allocation, bucketing, identity stability, and assignment logging, then rerun or recompute only after repair.

Likely label:

- `experiment_unreliable`

### 16.2 Assignment Clean, Refund Metric Imbalanced

User asks:

> Assignment counts are balanced, but refund users are heavily skewed toward treatment.

Good answer:

> The overall experiment may still be valid, but the refund metric is unreliable until the metric-level imbalance is diagnosed. Check refund event logging, joins, refund window maturity, and missingness by variant. Do not use refund as a guardrail until repaired.

Likely label:

- `metric_unreliable`

### 16.3 Triggered Analysis Bias

User asks:

> We analyzed only users who opened the new recommendation module. Treatment improved retention.

Good answer:

> This is likely post-treatment selection unless opening the module was equally observable and not affected by treatment. Use ITT or a pre-treatment trigger. Triggered retention cannot be interpreted as a clean causal effect if treatment changes the probability of entering the triggered population.

Likely label:

- `experiment_unreliable` for triggered readout

### 16.4 Segment-Localized SRM

User asks:

> SRM only appears on Android version 12. Other platforms are balanced.

Good answer:

> Diagnose Android version 12 separately. If the root cause is a treatment-specific logging or render issue on that version, do not include that segment in a broad launch claim. Restricted analysis may be possible only if the unaffected population is still representative and sufficiently powered.

Likely label:

- `metric_unreliable` or `experiment_unreliable`, depending on decision population

### 16.5 SRM After Ramp Change

User asks:

> SRM starts after day 4 when we ramped treatment from 10% to 50%.

Good answer:

> Check ramp configuration and assignment logs by day. If the allocation was changed unevenly or variants started at different times, the full-period result is unreliable. A clean pre-change or post-repair window may be analyzed only if independently balanced and sufficiently powered.

Likely label:

- `pipeline_blocker` or `experiment_unreliable`

---

## 17. Integration with Other Playbooks

SRM is a gatekeeper for other experimentation playbooks.

### 17.1 With `experiment_telemetry.md`

If SRM is detected:

- inspect assignment, exposure, trigger, event logging, metric lineage, and pipeline integrity;
- assign telemetry severity;
- preserve analysis recipe;
- do not interpret metric lift until trust status is resolved.

### 17.2 With `ab_testing.md`

If unresolved SRM exists:

- validity-first checks fail;
- the experiment should not be treated as causal evidence;
- statistical significance of business metrics is not sufficient.

### 17.3 With `launch_decision.md`

If unresolved SRM exists:

- use `do_not_trust_result`;
- do not recommend `launch` or `launch_with_monitoring` based on the experiment lift;
- recommend repair, rerun, or restricted analysis.

### 17.4 With `ads_experiments.md`

If SRM affects ad exposure, auction participation, or conversion attribution:

- do not claim incrementality;
- check impression eligibility, rendering, attribution window, advertiser segment, and privacy/consent filters.

### 17.5 With `marketplace_metrics.md`

If SRM affects buyer/seller assignment, listing exposure, market-level units, or shared inventory:

- ordinary unit-level estimates may be invalid;
- check marketplace interference and local-market imbalance;
- consider cluster, geo, or switchback design.

---

## 18. Evaluation Criteria for Agent Answers

A high-quality Agent answer should:

- identify expected allocation;
- compute or request observed allocation;
- run or describe an appropriate SRM test;
- distinguish assignment, exposure, trigger, metric, segment, and time-slice SRM;
- assign exactly one SRM severity label;
- avoid interpreting lift before diagnosis;
- identify likely root causes by experiment stage;
- state which metrics are reliable or unreliable;
- state whether causal analysis can proceed;
- recommend repair, rerun, restricted analysis, ITT, or metric exclusion;
- include an audit trail or analysis recipe;
- explain decision impact clearly.

Penalize an answer if it:

- recommends launch with unresolved SRM;
- says SRM is minor only because the business metric is significant;
- checks only final scorecard counts and ignores exposure or triggered populations;
- treats exposed-only analysis as causal when exposure is affected by treatment;
- ignores metric-level imbalance;
- ignores segment-level SRM;
- ignores ramp history or configuration changes;
- ignores mixed assignments;
- gives generic advice without severity classification;
- fails to specify next diagnostic steps;
- treats SRM as a p-value footnote rather than an evidence-validity failure.

---

## 19. Common Failure Modes

The Agent should avoid these failure modes:

1. **Lift-before-trust reasoning**

   Interpreting business metric movement before checking SRM.

2. **Ratio eyeballing**

   Looking only at observed percentages without considering sample size and statistical test.

3. **One-level SRM checking**

   Checking only final assignment counts while ignoring exposure, trigger, metric, segment, and time-slice populations.

4. **Triggered-analysis bias**

   Treating a post-treatment triggered population as if it preserved randomization.

5. **Metric contamination**

   Using a metric whose observation population has variant-specific missingness or duplication.

6. **Segment instability**

   Slicing by dynamic post-treatment segments and interpreting the result as pre-treatment heterogeneity.

7. **Result-shopping salvage**

   Restricting analysis to a clean-looking subset because it supports the desired conclusion.

8. **Unknown-root-cause optimism**

   Proceeding because the SRM "probably does not matter" without evidence.

9. **Pipeline blindness**

   Ignoring schema changes, backfills, late events, joins, or event version differences.

10. **Launch despite invalidity**

   Recommending broad launch because the treatment appears positive despite unresolved SRM.

---

## 20. Final Rule

SRM is not a business outcome. SRM is a warning that the experiment evidence chain may be broken.

If SRM is unresolved, the Agent must not use the experiment lift as causal launch evidence.

The correct action is to diagnose the root cause, repair the data or experiment, rerun if necessary, or restrict interpretation only to metrics and segments that remain valid after documented diagnosis.

A top data scientist does not ask only:

> Did treatment win?

A top data scientist asks first:

> Are the treatment and control populations trustworthy enough for the question to have a causal answer?

---

## External Methodology References

These references are included to help future maintainers understand the methodological background behind this playbook.

- Microsoft Research, "Diagnosing Sample Ratio Mismatch in A/B Testing."
- Fabijan et al. (KDD 2019), "Diagnosing Sample Ratio Mismatch in Online Controlled Experiments: A Taxonomy and Rules of Thumb for Practitioners."
- Microsoft Research, "Data Quality: Fundamental Building Blocks for Trustworthy A/B Testing Analysis."
- Microsoft Research, "Patterns of Trustworthy Experimentation: During-Experiment Stage."
- Eppo Documentation, "Sample Ratio Mismatch."
- Eppo Documentation, "Diagnostics."
- DoorDash Engineering, "Addressing the Challenges of Sample Ratio Mismatch in A/B Testing."
