# Experiment Telemetry Playbook

This playbook defines how the agent should audit experiment telemetry before interpreting experiment results.

It is designed for an evaluation-driven Agentic RAG system. The goal is not to teach the agent how to record events passively. The goal is to train the agent to act like an experiment evidence auditor: it should verify whether the full data path from randomization to scorecard is trustworthy enough to support causal analysis and product decisions.

The governing rule is:

> **No trusted telemetry, no trusted experiment, no responsible decision.**

A strong agent should not start by explaining a lift. It should first ask whether the lift is real, whether it was measured on the correct population, whether the events were captured consistently across variants, whether the metric is mature, and whether the experiment result can be reproduced by another analyst.

This playbook is especially important for launch decisions, A/B tests, ads experiments, marketplace experiments, recommendation experiments, policy experiments, and any automated product analytics workflow where the agent is expected to reason from experimental evidence.

---

## Quick Retrieval Summary

Use this playbook when the user asks whether an experiment result, scorecard, metric movement, telemetry pipeline, logging setup, or analysis population can be trusted.

This playbook is especially relevant when:

- the user asks whether an A/B test is valid;
- the result shows SRM, assignment imbalance, exposure imbalance, or logging imbalance;
- a metric moves sharply and may be a data artifact;
- CTR, conversion, retention, revenue, latency, refunds, or support tickets move unexpectedly;
- the experiment relies on triggered analysis, exposed-user analysis, or post-exposure filters;
- treatment and control may have different event logging behavior;
- assignment, exposure, trigger, or outcome definitions are unclear;
- events are delayed, duplicated, missing, backfilled, or affected by schema changes;
- the experiment spans platforms, devices, app versions, logged-in and logged-out identities, or privacy regimes;
- metric readouts are immature because the observation window is incomplete;
- the user asks for a launch decision but telemetry trust has not been established;
- the experiment pipeline was changed during the experiment;
- the agent needs to explain what evidence is reliable, what is unreliable, and what must be repaired or rerun.

Default reasoning order:

1. Reconstruct the experiment evidence chain.
2. Verify the telemetry contract.
3. Check assignment, exposure, trigger, and outcome alignment.
4. Run validity-first telemetry checks.
5. Classify analysis population: ITT, exposed, triggered, or per-protocol.
6. Audit metric lineage and ownership.
7. Check metric maturity and windowing.
8. Search for telemetry artifacts and adversarial explanations.
9. Check advanced bias risks.
10. Assign exactly one telemetry severity label.
11. State which metrics can and cannot be used.
12. Provide a reproducible analysis recipe.
13. Only then allow causal interpretation or launch-decision handoff.

---

## 1. Core Principle

Telemetry is the evidence infrastructure of experimentation.

An experiment result is not just a p-value, a confidence interval, or a metric lift. It is the final output of a chain:

```text
randomization
-> assignment event
-> exposure event
-> trigger event
-> outcome event
-> event ingestion
-> metric table
-> scorecard
-> decision
```

If any link in this chain is broken, ambiguous, variant-specific, or non-reproducible, the agent must downgrade trust.

The agent should treat telemetry failures as causal threats, not as minor implementation details.

Bad reasoning:

> Conversion increased by 3%, so the treatment probably worked.

Better reasoning:

> Conversion increased by 3%, but before interpreting this as a causal effect, we need to verify assignment balance, exposure consistency, outcome logging completeness, metric maturity, schema stability, and whether the analysis population was defined without post-treatment selection bias.

The agent should not reward itself for producing a confident answer when the evidence chain is broken.

---

## 2. Industry Context and Historical Lessons

Modern experimentation platforms at Microsoft, Airbnb, Netflix, LinkedIn, Google, Amazon, and other large-scale technology companies converged on a similar lesson: experimentation is not only a statistical problem. It is also a telemetry, platform, governance, and debugging problem.

Microsoft ExP emphasizes that Sample Ratio Mismatch should be tested before ship-decision analysis and that SRM is an end-to-end signal of severe quality issues. SRM can come from assignment, logging, execution, or analysis failures. A result with unresolved SRM should generally not be used for decision-making.

Airbnb's Experiment Reporting Framework was created to automate analytical heavy lifting and hide common pitfalls from experimenters. The important lesson for this playbook is that reliable experimentation requires standardized metrics, reusable analysis logic, and platform-level safeguards against common analytical mistakes.

Netflix describes A/B testing as a platform-supported process for comparing product experiences using control and treatment cells. The important lesson for telemetry is that experimentation must be supported by reproducible assignment, exposure, metric collection, and decision workflows, not by ad hoc event queries alone.

The agent should apply these lessons operationally:

- do not trust a metric movement before auditing telemetry;
- do not treat an experiment scorecard as self-validating;
- do not assume assignment, exposure, and outcome are aligned unless verified;
- do not assume triggered analysis is valid unless the trigger is pre-treatment and symmetric;
- do not allow launch decisions to depend on metrics with unresolved logging or maturity problems.

---

## 3. Telemetry Severity Labels

The agent must assign exactly one telemetry severity label.

Allowed labels:

- `clean`
- `minor_warning`
- `metric_unreliable`
- `experiment_unreliable`
- `pipeline_blocker`

The severity label determines whether causal analysis and launch decisions can proceed.

| Severity Label | Meaning | Can causal analysis proceed? | Can launch decision proceed? | Required Action |
|---|---|---:|---:|---|
| `clean` | No material telemetry issues found. The evidence chain is internally consistent. | Yes | Yes, subject to experiment result and business risk | Proceed to causal interpretation and decision playbook |
| `minor_warning` | Small telemetry warning exists, but it is unlikely to change the main conclusion. | Yes, with caveat | Yes, with caveat | State warning, monitor, and verify sensitivity |
| `metric_unreliable` | One or more metrics are unreliable, but the experiment may still be usable for other metrics. | Only for reliable metrics | Only if decision does not depend on unreliable metrics | Exclude or repair affected metric |
| `experiment_unreliable` | Core assignment, exposure, trigger, or logging issues make the experiment invalid as causal evidence. | No | No | Diagnose root cause, repair, rerun, or reanalyze from valid population |
| `pipeline_blocker` | Data pipeline, schema, identity, or ingestion failure prevents trustworthy analysis. | No | No | Stop analysis and fix pipeline before interpreting results |

Do not use multiple primary labels. If multiple issues exist, choose the most severe label.

Severity ordering:

```text
clean < minor_warning < metric_unreliable < experiment_unreliable < pipeline_blocker
```

---

## 4. Label Boundary Rules

### 4.1 `clean`

Use `clean` when:

- assignment counts match expected allocation;
- exposure logging is consistent across variants;
- trigger definition is symmetric and not treatment-induced;
- outcome events are logged consistently;
- metric lineage is known;
- metric windows are mature;
- no major schema, pipeline, identity, or platform imbalance exists;
- analysis can be reproduced.

The agent may proceed to causal analysis.

---

### 4.2 `minor_warning`

Use `minor_warning` when:

- the issue is small, understood, and unlikely to affect the decision;
- the affected metric is diagnostic rather than decision-critical;
- a small amount of late-arriving data exists but mature metrics are unaffected;
- a platform/version imbalance is present but controlled by stratified checks and does not affect results;
- the warning has a clear sensitivity analysis.

Example:

> Minor warning: mobile app version 8.3 is slightly overrepresented in treatment, but the imbalance is small and the primary metric is stable when excluding that version. Causal analysis can proceed with caveat.

---

### 4.3 `metric_unreliable`

Use `metric_unreliable` when a specific metric cannot be trusted but the entire experiment is not necessarily invalid.

Examples:

- purchase event logging changed mid-experiment;
- refund metric is not mature yet;
- one diagnostic event is duplicated in treatment;
- a client-only event is missing on one platform;
- an attribution window changed for ads conversions;
- support-ticket metric has incomplete ingestion.

The agent should not use the unreliable metric as evidence for launch or no-launch. It may still analyze other reliable metrics.

---

### 4.4 `experiment_unreliable`

Use `experiment_unreliable` when the core causal comparison is compromised.

Examples:

- unresolved assignment SRM;
- randomization unit mismatch;
- treatment/control exposure definitions differ;
- treatment causes users to enter or exit the analysis population;
- outcome logging differs by variant for decision-critical metrics;
- treatment leaks into control;
- triggered analysis is based on a treatment-induced trigger;
- identity resolution differs by variant;
- variant-specific logging loss affects most metrics.

The agent should use `do_not_trust_result` if handing off to a launch decision playbook.

---

### 4.5 `pipeline_blocker`

Use `pipeline_blocker` when the data pipeline itself prevents meaningful analysis.

Examples:

- assignment table missing or corrupted;
- metric table was backfilled incorrectly;
- schema changed without versioning;
- ingestion job failed for one variant;
- event timestamps were shifted or truncated;
- scorecard was generated from mixed metric versions;
- identity mapping table changed during the experiment;
- no reproducible analysis dataset exists.

The correct next step is pipeline repair, not metric interpretation.

---

## 5. Telemetry Contract

Every experiment must have a telemetry contract before results are interpreted.

The contract defines what must be true for the experiment data to be considered valid.

### 5.1 Required Contract Fields

| Contract Field | Definition | Agent Must Check |
|---|---|---|
| Experiment ID | Stable identifier for experiment configuration and analysis | Same ID across assignment, exposure, event, and scorecard tables |
| Randomization unit | Unit assigned to variants, such as user, device, account, session, query, geo, or cluster | Matches analysis unit or is correctly aggregated |
| Assignment event | Record that a unit was allocated to control/treatment | Logged once, stable, timestamped, and not post-treatment |
| Exposure event | Record that the unit actually experienced the variant | Consistent definition across variants |
| Trigger event | Event that makes a unit relevant for analysis | Symmetric and not treatment-induced |
| Outcome event | Event used to construct metrics | Logged consistently across variants |
| Analysis population | Units included in analysis | Defined before reading outcomes |
| Metric window | Time window over which outcomes are counted | Mature and aligned with metric definition |
| Event timestamp | Time when user action occurred | Not confused with ingestion timestamp |
| Ingestion timestamp | Time when event entered data warehouse | Used to assess lateness and completeness |
| Attribution timestamp | Time used to attribute conversion or outcome | Consistent across variants |
| Schema contract | Required fields, types, versions, and nullability | Stable during experiment |
| Metric owner | Team or system responsible for metric definition | Known for decision-critical metrics |
| Metric version | Versioned metric logic | Same version used for treatment/control |

---

### 5.2 Agent Action: Contract Reconstruction

The agent should reconstruct the contract in this order:

1. What unit was randomized?
2. What event recorded assignment?
3. What event recorded exposure?
4. What event defined triggering?
5. What events produced the decision metrics?
6. What population was analyzed?
7. What windows and attribution rules were used?
8. What schemas and metric versions were active?
9. Can another analyst reproduce the result from the same tables?

If the agent cannot answer these questions, it should not produce a causal interpretation.

Required output:

```text
Telemetry contract status:
- Randomization unit:
- Assignment event:
- Exposure event:
- Trigger event:
- Outcome events:
- Analysis population:
- Metric windows:
- Schema / metric version:
- Owner:
- Reproducibility status:
```

---

### 5.3 Agent Must Not

The agent must not:

- infer causality from a metric table without checking assignment and exposure;
- treat exposed-user analysis as automatically valid;
- mix user-level assignment with event-level outcomes without correct aggregation;
- analyze triggered users if the trigger is affected by treatment;
- trust a scorecard when the underlying metric definition is unknown;
- ignore metric version changes;
- assume event timestamps and ingestion timestamps are equivalent;
- recommend launch when the telemetry contract is ambiguous.

---

## 6. Validity-First Telemetry Checks

Before interpreting any metric movement, the agent must run validity-first checks.

The agent should output telemetry status before metric readout.

### 6.1 Mandatory Validity Checklist

| Check | Question | Failure Risk | Typical Severity |
|---|---|---|---|
| Assignment SRM | Do observed assignment counts match configured allocation? | Randomization, logging, eligibility, or analysis failure | `experiment_unreliable` |
| Exposure SRM | Do exposed users match expected variant ratios? | Variant load failure, exposure logging difference | `experiment_unreliable` |
| Triggered-population imbalance | Are triggered units balanced? | Trigger may be treatment-induced | `experiment_unreliable` or `metric_unreliable` |
| Pre-treatment covariate balance | Are key baseline attributes balanced? | Randomization or sample construction failure | `experiment_unreliable` |
| Logging completeness | Are expected events present by variant? | Missing outcomes or biased metrics | `metric_unreliable` or worse |
| Event duplication | Are duplicate events balanced across variants? | Artificial metric inflation | `metric_unreliable` |
| Missingness by variant | Are nulls/missing events variant-specific? | MNAR and biased estimates | `metric_unreliable` or worse |
| Client/server mismatch | Do client and server events agree? | Partial logging or platform bug | `metric_unreliable` |
| Platform/version balance | Are app versions, browsers, OS, and platforms balanced? | Release or eligibility confounding | `minor_warning` to `experiment_unreliable` |
| Bot/spam imbalance | Are abnormal users or bots balanced? | Fake lift or fake degradation | `metric_unreliable` |
| Timezone/window alignment | Are windows defined consistently? | Miscounted days, retention, or conversions | `metric_unreliable` |
| Late-arriving events | Are all metrics sufficiently complete? | Immature metrics | `metric_unreliable` |
| Pipeline stability | Did ETL, backfill, or refresh logic change? | Non-reproducible scorecard | `pipeline_blocker` |
| Instrumentation stability | Did event names, schemas, or emitters change? | Broken metric lineage | `metric_unreliable` or `pipeline_blocker` |
| Identity stability | Did device/user/account mapping change? | Misassigned users or cross-device contamination | `experiment_unreliable` |
| Treatment contamination | Did control units receive treatment? | Biased comparison | `experiment_unreliable` |
| Privacy/Opt-out balance | Are tracking opt-outs (e.g., iOS ATT) balanced across variants? | Treatment-induced missingness (MNAR) | `experiment_unreliable` |

---

### 6.2 SRM Interpretation

Sample Ratio Mismatch is not merely a count discrepancy. It is a symptom that the experiment data path may be broken.

Potential SRM causes:

- randomization bug;
- eligibility filter differs across variants;
- assignment event missing in one variant;
- exposure event logged differently;
- treatment causes app crash or render failure;
- bot or spam traffic unevenly assigned;
- device ID or user ID read differently by variant;
- post-assignment filtering removes users unevenly;
- event ingestion fails for one group;
- analysis query joins drop one variant more often.

Agent rule:

> If unresolved assignment SRM exists, do not interpret treatment effects as causal evidence.

The measured lift may be directionally interesting for debugging, but it is not a launch signal.

---

### 6.3 Metric-Level SRM

Overall assignment may look balanced while metric observation units are imbalanced.

Examples:

- page-load metric has more observations in treatment because treatment generates extra page loads;
- latency metric includes only successful renders, and treatment has more render failures;
- purchase metric includes only users reaching checkout, but treatment changes who reaches checkout;
- support-ticket metric captures only users who authenticate, and login behavior differs by variant.

Agent action:

- check SRM at the unit level used by each metric;
- identify whether the metric population is pre-treatment or post-treatment;
- determine whether imbalance is expected mechanism or telemetry failure;
- downgrade only affected metrics if the experiment assignment is otherwise clean.

---

## 7. Analysis Population Logic

The agent must distinguish the population being analyzed.

Different populations answer different questions.

### 7.1 Population Types

| Population | Definition | Causal Question | Main Risk |
|---|---|---|---|
| ITT | All assigned units | Effect of assignment to treatment | Dilution from non-exposure |
| Exposed-user analysis | Units that saw the treatment/control experience | Effect among exposed units | Exposure may be treatment-induced |
| Triggered analysis | Units satisfying a relevance trigger | Effect among units for whom experiment is relevant | Trigger must be symmetric and not treatment-affected |
| Per-protocol analysis | Units who complied with assigned experience | Effect among compliers | Strong post-treatment selection risk |
| Eligible population | Units meeting pre-treatment eligibility | Effect among eligible units | Eligibility drift or misclassification |
| Shadow population | Units who would have been eligible or triggered but were not included in main scorecard | Detects filtering bias and eligibility drift | Requires logging counterfactual inclusion logic |

---

### 7.2 ITT Analysis

Intent-to-treat analysis includes all randomized units, regardless of whether they were exposed.

Use ITT when:

- exposure is not consistently logged;
- exposure may be affected by treatment;
- the decision is about rolling out assignment to the whole eligible population;
- you need a conservative estimate of policy impact.

Limitations:

- effect may be diluted by users who never encounter the feature;
- may be insensitive for rare triggers;
- may hide mechanism.

Agent action:

- use ITT as default when triggered analysis is questionable;
- do not discard unexposed users unless exposure logic is clearly pre-specified and symmetric.

---

### 7.3 Triggered Analysis

Triggered analysis includes only units for whom the experiment was relevant.

It can improve sensitivity, but only when the trigger is valid.

A valid trigger should be:

- defined before outcome measurement;
- logged consistently in control and treatment;
- based on pre-treatment or treatment-invariant conditions;
- not caused by treatment;
- not affected by variant load speed, UI placement, or user behavior changed by treatment.

Good trigger examples:

- user issued a search query before seeing ranking treatment;
- user visited a product page before recommendation module was shown;
- user was eligible based on pre-existing account status;
- geo was assigned before policy exposure.

Invalid trigger examples:

- user clicked the treatment module;
- user saw a treatment-only UI element;
- user entered checkout because treatment made checkout easier;
- user loaded a page that treatment makes faster or slower;
- user was included only if treatment successfully rendered.

Agent rule:

> If the trigger is affected by treatment, triggered analysis creates post-treatment selection bias.

When triggered analysis fails, use ITT or redesign exposure logging.

---

### 7.4 Exposed-User Analysis

Exposed-user analysis can be useful for mechanism, but it is dangerous for decision-making if exposure depends on treatment.

Ask:

- Was exposure opportunity symmetric?
- Did both variants log exposure using the same code path?
- Can treatment change the probability of exposure?
- Are unexposed assigned users excluded differently by variant?
- Does variant load failure remove users from the exposed population?

If exposure itself is affected by treatment, exposed-user analysis may estimate a selected subgroup rather than the treatment effect.

---

### 7.5 Per-Protocol Analysis

Per-protocol analysis should be treated as diagnostic unless the compliance mechanism is well understood.

It often introduces post-treatment selection bias because compliance may be affected by the treatment.

Agent should not use per-protocol results as primary launch evidence unless supported by strong design justification.

---

### 7.6 Shadow Population Integrity Audit
Top-tier auditing requires checking the "Untriggered" population to detect hidden Selection Bias.
- **Agent Action:** Compare the baseline attributes (e.g., pre-experiment activity) of users who were assigned but *not* triggered/exposed. 
- **Risk:** If Treatment "untriggered" users are significantly higher quality than Control "untriggered" users, it implies the Treatment logic is "pushing out" low-quality users from the analysis population, creating a fake lift.
- **Decision:** If shadow population imbalance exists, downgrade to `experiment_unreliable`.

---

## 8. Metric Lineage and Ownership

The agent must know where every decision-critical metric comes from.

A metric name is not enough.

### 8.1 Required Metric Lineage Fields

For each metric, document:

- metric name;
- metric category: decision, success, guardrail, diagnostic, system, quality, or long-term proxy;
- raw event source;
- event emitter: client, server, backend job, partner system, payment processor, ads system, CRM, support system;
- join keys;
- deduplication rules;
- filters;
- attribution window;
- sessionization rules;
- numerator definition;
- denominator definition;
- aggregation unit;
- metric owner;
- metric version;
- schema version;
- null handling;
- timezone;
- freshness SLA;
- historical definition consistency.

---

### 8.2 Standard vs Ad Hoc Metrics

The agent should distinguish:

| Metric Type | Description | Trust Level |
|---|---|---|
| Standard platform metric | Versioned, owned, widely reused, monitored | Higher |
| Team-owned standard metric | Owned and versioned by one product team | Medium to high |
| Experiment-specific metric | Created for one experiment with documented lineage | Medium |
| Ad hoc query metric | Constructed from raw events without stable ownership | Lower |
| Debug metric | Useful for diagnosis but not decision-critical | Diagnostic only |

Agent rule:

> Do not let an ad hoc metric override a standard decision metric unless the metric definition, lineage, and validation are explicitly documented.

---

### 8.3 Metric Ownership Questions

The agent should ask:

- Who owns the metric?
- Is the metric versioned?
- Has the metric definition changed recently?
- Is the metric used in other experiments?
- Are treatment and control using the same schema?
- Was the metric backfilled?
- Does the metric rely on a join that can drop users unevenly?
- Does the metric depend on client-side events that can be blocked or delayed?
- Is the metric known to be sensitive to bots, retries, or duplicate events?

---

## 9. Timeliness and Window Governance

Many experiment conclusions are wrong because the metric window is incomplete.

The agent must classify metric maturity before interpreting results.

### 9.1 Metric Maturity Labels

Use these labels at the metric level:

- `mature`
- `partially_mature`
- `not_mature_yet`
- `stale_or_backfilled`
- `unknown_maturity`

| Maturity Label | Meaning | Agent Action |
|---|---|---|
| `mature` | Observation window is complete and ingestion lag has passed | Can interpret |
| `partially_mature` | Some data has arrived but full window is incomplete | Interpret only as early signal |
| `not_mature_yet` | Required outcome window has not passed | Do not use for final decision |
| `stale_or_backfilled` | Data freshness or backfill may distort comparison | Validate before use |
| `unknown_maturity` | Freshness or window logic unavailable | Downgrade trust |

---

### 9.2 Metric Lag Classes

| Lag Class | Examples | Common Risk |
|---|---|---|
| Fast metrics | impressions, clicks, render success, exposure, latency, crash, API error | Duplicate logging, render failure, bot traffic |
| Medium-lag metrics | signup, activation, add-to-cart, checkout, booking, first purchase | Conversion window may be incomplete |
| Long-lag metrics | 7-day retention, 28-day retention, refund, chargeback, complaint, support ticket, advertiser conversion, LTV | Early readout is biased or immature |
| Very long-lag metrics | subscription churn, advertiser retention, seller retention, creator quality, marketplace health | Requires holdout or post-launch monitoring |

---

### 9.3 Timestamp Governance

The agent must distinguish:

- event timestamp: when the user action occurred;
- ingestion timestamp: when the event arrived in the warehouse;
- processing timestamp: when the pipeline transformed the event;
- attribution timestamp: when the event is attributed to a session, ad, user, campaign, or experiment;
- scorecard timestamp: when results were computed.

Failure pattern:

> Purchase event timestamp is correct, but ingestion is delayed more in treatment because the treatment uses a new checkout API. Early purchase conversion appears lower in treatment, but this may be a delayed-ingestion artifact.

Agent action:

- check late-arrival curves by variant;
- compare event timestamp vs ingestion timestamp;
- require maturity for delayed metrics;
- do not use immature long-lag metrics for launch decisions.

---

## 10. System Hygiene

Telemetry failures often come from system behavior, not from statistical analysis.

The agent must check whether the experiment variants changed the ability to observe users.

### 10.1 System Hygiene Checklist

| Area | Agent Must Check |
|---|---|
| Render success | Did treatment/control render successfully at similar rates? |
| Variant load | Did one variant fail to load or time out more often? |
| Latency | Did treatment delay exposure, event logging, or conversion? |
| API errors | Did backend errors differ by variant? |
| Client crashes | Did one variant crash before outcome events could be logged? |
| Event send success | Did client events reach the pipeline equally? |
| Feature flag | Was the flag evaluated consistently? |
| App version | Was treatment available only on some versions? |
| Browser/OS | Did compatibility differ by variant? |
| Identity resolution | Did device ID, user ID, cookie, or account ID mapping differ? |
| Logged-in status | Did logged-in and logged-out users mix inconsistently? |
| Privacy settings | Did consent or tracking restrictions affect variants differently? |
| Bot filtering | Was abnormal traffic removed symmetrically? |

---

### 10.2 Variant Load Failure

A treatment can look bad because the product is bad, but it can also look bad because the variant failed to load.

Agent must check:

- assignment count;
- exposure count;
- render-success count;
- page-load latency;
- crash rate;
- API error rate;
- event-send success;
- drop-off before exposure;
- platform/version-specific failures.

If treatment load failure changes who enters the analysis population, the experiment may be `experiment_unreliable`.

---

## 11. Adversarial Telemetry Debugging

The agent should behave like a skeptical auditor.

When a metric moves, first search for non-causal telemetry explanations.

### 11.1 Debugging Pattern: CTR Spike

If CTR increases sharply, check:

- duplicate click logging;
- accidental clicks;
- larger clickable area;
- UI shift causing misclicks;
- ad slot movement;
- click event fired on impression;
- bot traffic;
- low-quality sessions;
- scroll-depth change;
- impression denominator change;
- click attribution window change;
- client event retries;
- platform-specific event bug.

Do not conclude improved relevance until these are checked.

---

### 11.2 Debugging Pattern: Conversion Drop

If conversion drops sharply, check:

- purchase event missing or delayed;
- attribution window shortened;
- payment logging failure;
- checkout API latency;
- treatment-specific checkout errors;
- variant load failure;
- join failure between exposure and purchase;
- server-side event still using old experiment ID;
- delayed ingestion;
- platform/version-specific payment bug.

Do not conclude user demand decreased until these are checked.

---

### 11.3 Debugging Pattern: Retention Lift

If retention improves unexpectedly, check:

- inactive users excluded differently;
- bots filtered only in one group;
- denominator changed;
- notification or email exposure not logged;
- experiment changed login persistence;
- identity stitching caused returning users to be counted differently;
- retention window incomplete;
- timezone boundary issue;
- app version imbalance;
- reactivation events counted as retention.

---

### 11.4 Debugging Pattern: Revenue Lift

If revenue increases, check:

- tax/shipping/fee treatment changed metric definition;
- currency conversion changed;
- refund and chargeback windows incomplete;
- duplicate payment events;
- large outlier orders;
- business accounts unevenly assigned;
- attribution to experiment differs by variant;
- revenue shifted from another surface;
- delayed cancellation metrics not mature.

---

### 11.5 Debugging Pattern: Latency Regression

If latency worsens, check:

- metric observation population changed;
- treatment generated extra page loads;
- failed renders excluded from latency metric;
- client-side and server-side timestamps differ;
- cache state differs;
- version rollout overlapped with experiment;
- geography/CDN imbalance;
- event recorded after extra client work in treatment.

---

## 12. Advanced Bias Checks

Top-level telemetry auditing must go beyond standard SRM.

### 12.1 Config Snapshot

The agent should require a configuration snapshot for each experiment run.

The snapshot should include:

- experiment ID;
- variant allocation;
- targeting and eligibility rules;
- start and end time;
- randomization unit;
- salt or hash configuration;
- feature flag version;
- treatment parameters;
- app version constraints;
- platform constraints;
- metric configuration;
- exposure event definition;
- trigger definition;
- rollout percentage changes;
- mid-experiment changes.

Agent rule:

> If experiment configuration changed mid-run and the analysis does not account for it, downgrade severity.

- **Config Drift Detection:** The Agent must explicitly check if feature flag parameters or allocation percentages changed during the active data window. If a "mid-flight" change occurred without a corresponding reset in the analysis start-time, the Agent must flag this as a `pipeline_blocker` or `minor_warning` depending on the magnitude.

---

### 12.2 Shadow Population Monitoring

A shadow population is a monitored set of users, sessions, or events that should have been eligible, triggered, or exposed but may not appear in the main analysis.

Use shadow population monitoring to detect:

- treatment-specific filtering;
- eligibility drift;
- exposure leakage;
- dropped users after assignment;
- users who fail to render treatment;
- users who trigger the experiment but are excluded from scorecard;
- users affected by privacy or consent settings;
- users with missing IDs.

Agent action:

- compare assigned population, eligible population, exposed population, triggered population, and analyzed population;
- compute drop-off rates at every stage by variant;
- flag variant-specific attrition.

---

### 12.3 MNAR: Missing Not At Random

Missing data is dangerous when missingness is caused by treatment or correlated with outcome.

Examples:

- treatment increases page latency, causing users to quit before outcome logging;
- iOS privacy settings block certain events more for one variant;
- treatment changes login state and breaks identity joins;
- users with failed purchases are missing purchase-confirmation events;
- crash prevents event emission.

Agent rule:

> Variant-specific missingness should be treated as a potential causal and telemetry failure, not as harmless missing data.

---

### 12.4 Privacy and Consent Effects

Privacy rules, consent flows, and platform restrictions can change what is observed.

Agent must check:

- consent opt-in balance;
- iOS App Tracking Transparency differences;
- cookie availability;
- logged-in vs logged-out identity;
- cross-device identity loss;
- tracking prevention by browser;
- third-party attribution restrictions;
- server-side vs client-side event availability.

If privacy or consent affects outcome visibility differently by variant, the affected metrics may be unreliable.

---

### 12.5 Feature Flag and Exposure Leakage

Feature flags can create telemetry bias if assignment and actual treatment do not match.

Check:

- assigned variant vs served variant;
- served variant vs rendered variant;
- rendered variant vs exposure log;
- exposure log vs outcome attribution;
- treatment parameters at time of exposure;
- cache behavior;
- stale configuration;
- fallback paths;
- control users accidentally receiving treatment;
- treatment users falling back to control.

---

## 13. Telemetry Failure Decision Matrix

| Failure Pattern | Typical Severity | Agent Action |
|---|---|---|
| Assignment SRM with unknown root cause | `experiment_unreliable` | Do not interpret lift; diagnose assignment/logging/filtering |
| Assignment table missing or corrupted | `pipeline_blocker` | Stop analysis; repair assignment source |
| Exposure counts imbalanced because treatment fails to render | `experiment_unreliable` | Do not use exposed-only result; inspect render failure |
| Trigger condition depends on treatment behavior | `experiment_unreliable` | Avoid triggered analysis; use ITT or redesign trigger |
| Outcome event missing only in treatment | `metric_unreliable` or `experiment_unreliable` | Exclude affected metric; rerun if decision-critical |
| Duplicate click events in treatment | `metric_unreliable` | Do not use CTR/click metrics; deduplicate and revalidate |
| Long-lag metric window incomplete | `metric_unreliable` | Mark `not_mature_yet`; do not use for final launch |
| Schema changed mid-experiment | `pipeline_blocker` | Recompute from versioned schema or rerun |
| Pipeline backfill during experiment | `pipeline_blocker` or `metric_unreliable` | Verify reproducibility and rerun scorecard |
| Platform/app version imbalance | `minor_warning` to `experiment_unreliable` | Stratify by version; check if imbalance changes conclusions |
| Bot imbalance | `metric_unreliable` | Filter symmetrically and rerun sensitivity |
| Client/server event mismatch | `metric_unreliable` | Prefer authoritative source if validated |
| Metric owner unknown for decision metric | `minor_warning` or `metric_unreliable` | Treat metric as lower-trust until lineage is documented |
| Event timestamp and ingestion timestamp confused | `metric_unreliable` | Recompute using correct time semantics |
| Variant-specific identity resolution | `experiment_unreliable` | Do not trust user-level outcomes |
| Treatment contamination in control | `experiment_unreliable` | Estimate contamination; rerun if material |
| Config changed without snapshot | `pipeline_blocker` | Recover configuration or rerun |

---

## 14. Decision Rules

### 14.1 Trust Before Lift

The agent must not interpret metric movement before telemetry trust is established.

Bad:

> CTR increased 8%, but there may be a logging issue.

Better:

> CTR increased 8%, but click duplication is variant-specific. CTR is `metric_unreliable`; this lift should not be used as product evidence.

---

### 14.2 Metric-Level Trust

Not all metrics fail together.

If assignment and exposure are clean but one metric is broken, the agent should label only that metric unreliable.

Example:

> Assignment and exposure pass. Activation and latency are reliable. Purchase conversion is not mature because the 7-day attribution window is incomplete. Causal analysis can proceed for activation and latency, but not for purchase conversion.

---

### 14.3 Experiment-Level Trust

If assignment, exposure, or trigger validity fails, the whole experiment may be unreliable.

Example:

> Triggered analysis is invalid because treatment increases the probability of triggering. The triggered population is post-treatment selected. The experiment result should not be used as causal evidence.

---

### 14.4 Pipeline Blocker

If data cannot be reproduced, do not interpret results.

Example:

> The scorecard used a metric table generated before a backfill, while the raw event table now produces different counts. This is a `pipeline_blocker`. Repair and rerun before interpreting effects.

---

## 15. Scenario Playbooks

### 15.1 Search Ranking Experiment

Common telemetry risks:

- query-level vs user-level randomization mismatch;
- triggered population defined by search behavior affected by ranking;
- exposure event missing for failed search results;
- latency changes affect query volume;
- click metrics inflated by UI layout changes;
- downstream conversion window incomplete.

Agent action:

- verify randomization unit;
- check query/user aggregation;
- use pre-treatment search intent where possible;
- inspect render success and latency;
- treat CTR as diagnostic unless lineage is clean;
- check downstream retention and conversion maturity.

---

### 15.2 Recommendation System Experiment

Common telemetry risks:

- exposure defined by seeing a recommendation module;
- treatment changes the number of recommendations shown;
- impression denominator changes;
- click or dwell time is duplicated;
- treatment affects session length and therefore observation volume;
- content quality metrics lag;
- creator or marketplace effects not captured in user scorecard.

Agent action:

- compare assignment, exposure, and impression opportunities;
- audit impression and click lineage;
- check sessionization changes;
- check quality and long-term metrics maturity;
- flag diagnostic engagement metrics if denominator changed.

---

### 15.3 Ads Experiment

Common telemetry risks:

- attribution window mismatch;
- delayed advertiser conversions;
- ad load changes impression denominator;
- click spam or accidental clicks;
- auction dynamics alter who is exposed;
- privacy restrictions affect conversion visibility;
- revenue lift may precede advertiser ROI degradation.

Agent action:

- verify impression, click, conversion, and revenue lineage;
- check advertiser conversion maturity;
- separate platform revenue from advertiser value;
- audit attribution timestamp and conversion window;
- detect bot/click-spam imbalance;
- flag short-term revenue if refund, churn, or ROI metrics are immature.

---

### 15.4 Checkout or Payment Experiment

Common telemetry risks:

- payment confirmation event delayed;
- failure events not logged symmetrically;
- refund/chargeback not mature;
- payment provider events join incorrectly;
- treatment changes redirect or authentication flow;
- app/web version imbalance.

Agent action:

- reconcile client checkout, server order, payment processor, refund, and support events;
- check latency and error rates;
- confirm conversion window maturity;
- inspect join keys and dedup rules;
- treat revenue lift as incomplete until refunds mature if risk is material.

---

### 15.5 Notification or Email Experiment

Common telemetry risks:

- assignment at user level but exposure at message level;
- send, delivered, opened, clicked, and conversion events are confused;
- treatment changes deliverability;
- opt-out and unsubscribe metrics lag;
- notification fatigue appears after short window;
- bot opens or email client prefetch affects open rate.

Agent action:

- separate send, delivery, open, click, and downstream outcomes;
- check denominator consistency;
- treat opens as diagnostic;
- require unsubscribe, mute, complaint, and retention guardrails;
- mark long-term fatigue metrics as not mature if window is short.

---

### 15.6 Marketplace Experiment

Common telemetry risks:

- treated buyers affect untreated sellers;
- seller supply shifts across variants;
- item inventory is shared;
- conversion gain comes from crowding out control;
- refunds/cancellations lag;
- liquidity metrics require longer windows.

Agent action:

- check interference risk;
- compare buyer and seller populations;
- audit transaction, cancellation, refund, and support lineage;
- consider cluster, geo, or switchback design if user-level randomization contaminates control;
- mark marketplace-health metrics as long-lag.

---

### 15.7 Policy or Eligibility Experiment

Common telemetry risks:

- policy changes who is eligible;
- treatment induces missingness;
- user behavior changes before exposure;
- enforcement logs are incomplete;
- appeals/support outcomes lag;
- fairness segments have small samples.

Agent action:

- separate assignment, eligibility, enforcement, exposure, and outcome events;
- check shadow population;
- detect anticipation and spillover if relevant;
- require audit logs and policy configuration snapshots;
- avoid causal claims if treatment changes inclusion in analysis population.

---

## 16. Required Response Template for the Agent

When answering telemetry trust questions, use this template.

```text
Telemetry Status:
[clean / minor_warning / metric_unreliable / experiment_unreliable / pipeline_blocker]

Can causal analysis proceed?
[yes / no / only for specific metrics]

Can launch decision proceed from this experiment?
[yes / no / only with caveat / only after rerun]

Experiment evidence chain:
- Randomization:
- Assignment:
- Exposure:
- Trigger:
- Outcome:
- Metric table:
- Scorecard:

Telemetry contract:
- Randomization unit:
- Assignment event:
- Exposure event:
- Trigger event:
- Outcome events:
- Analysis population:
- Metric windows:
- Schema / metric versions:
- Metric owners:

Validity checks:
1. Assignment SRM:
2. Exposure imbalance:
3. Triggered-population imbalance:
4. Logging completeness:
5. Event duplication:
6. Missingness by variant:
7. Platform/version balance:
8. Bot/spam imbalance:
9. Metric maturity:
10. Pipeline/schema stability:

Reliable metrics:
- [metric]: [why reliable]

Unreliable metrics:
- [metric]: [why unreliable]

Adversarial debugging:
- [artifact risk checked]
- [artifact risk checked]

Analysis recipe:
- assignment/exposure/event tables: [source_table_names]
- config snapshot version: [commit_id_or_timestamp]
- shadow population check: [pass/fail/imbalance_magnitude]
- privacy missingness check: [pass/fail/diff_percentage]
- agent reasoning hash: [unique_id_for_this_audit_logic]
- reproducibility status: [fully_reproducible / ad_hoc_risk]

Recommendation:
[clear action: proceed / exclude metric / diagnose / rerun / repair pipeline]
```

---

## 17. Minimum Evidence Required for Telemetry Audit

A telemetry audit should include:

### 17.1 Experiment Identity

- experiment ID;
- variant names;
- configured allocation;
- start and end dates;
- product surface;
- owner;
- config snapshot.

### 17.2 Assignment and Exposure

- randomization unit;
- assignment counts;
- exposure counts;
- assignment-to-exposure drop-off;
- feature flag consistency;
- render success;
- contamination check.

### 17.3 Triggering and Analysis Population

- trigger definition;
- trigger symmetry;
- trigger timing;
- analysis population;
- excluded users or events;
- shadow population if available.

### 17.4 Metric Lineage

- raw events;
- event emitters;
- joins;
- filters;
- dedup logic;
- windows;
- aggregation unit;
- schema and metric versions;
- owner.

### 17.5 System and Pipeline Health

- ingestion completeness;
- late events;
- pipeline refresh;
- backfills;
- schema changes;
- client/server consistency;
- platform/app version balance;
- bot/spam filters.

### 17.6 Final Audit Output

- severity label;
- reliable metrics;
- unreliable metrics;
- missing evidence;
- required repair or rerun;
- analysis recipe.

---

## 18. Evaluation Criteria for Agent Answers

A high-quality answer should:

- assign exactly one telemetry severity label;
- check telemetry before interpreting metric lift;
- reconstruct the experiment evidence chain;
- distinguish assignment, exposure, trigger, and outcome;
- classify the analysis population;
- detect invalid triggered analysis;
- identify SRM or metric-level imbalance;
- check logging completeness and duplication;
- check variant-specific missingness;
- check metric maturity;
- document metric lineage;
- provide reliable and unreliable metric lists;
- include an analysis recipe;
- avoid causal claims from broken telemetry;
- state the next repair, rerun, or diagnostic action.

Penalize an answer if it:

- recommends launch before telemetry checks;
- interprets p-values before SRM;
- ignores assignment/exposure/trigger differences;
- uses exposed-only analysis when exposure is treatment-induced;
- treats telemetry artifacts as product effects;
- ignores delayed conversions or retention windows;
- ignores schema or pipeline changes;
- fails to identify treatment-induced filtering;
- gives generic advice without severity classification;
- fails to state which metrics are reliable;
- fails to provide reproducibility details;
- treats a scorecard as trustworthy because it exists.

A strong answer should feel like a senior data scientist reviewing whether the experiment evidence can be admitted into decision-making.

---

## 19. Common Failure Modes

The agent should avoid these failure modes:

1. **P-value before telemetry**

   Interpreting statistical significance before checking assignment, exposure, trigger, and logging validity.

2. **Metric lift without lineage**

   Treating a named metric as valid without knowing raw events, joins, filters, and metric version.

3. **Exposed-only bias**

   Analyzing only exposed users when exposure probability is affected by treatment.

4. **Invalid triggered analysis**

   Using a trigger that treatment itself changes.

5. **Ignoring delayed outcomes**

   Treating early retention, refund, chargeback, advertiser conversion, or LTV as final before the window matures.

6. **Variant-specific logging blindness**

   Missing that treatment and control emit events through different code paths.

7. **Data artifact explanation failure**

   Explaining CTR spikes or conversion drops as product effects without checking duplicate events, accidental clicks, latency, or ingestion delay.

8. **Pipeline trust fallacy**

   Assuming the scorecard is correct because it was generated by a pipeline.

9. **Identity instability**

   Ignoring cookie, device ID, account ID, logged-in state, or cross-device mapping changes.

10. **Config drift**

   Ignoring mid-experiment allocation, eligibility, feature flag, or treatment parameter changes.

11. **Overclaiming under uncertainty**

   Giving a confident launch or no-launch recommendation when telemetry trust is incomplete.

12. **Metric-level and experiment-level confusion**

   Invalidating the whole experiment when only one metric is broken, or trusting the whole experiment when the assignment layer is broken.

---

## 20. Agent Action Checklist

Before interpreting any experiment result, the agent must check:

```text
[ ] What unit was randomized?
[ ] Are assignment counts consistent with expected allocation?
[ ] Is assignment stable over time?
[ ] Is exposure defined and logged consistently across variants?
[ ] Is the trigger symmetric and not affected by treatment?
[ ] Is the analysis population pre-specified?
[ ] Are outcome events logged through the same code path?
[ ] Are missing events balanced across variants?
[ ] Are duplicate events balanced across variants?
[ ] Are app version, platform, geography, and device distributions balanced?
[ ] Are bot/spam filters applied symmetrically?
[ ] Are event timestamps, ingestion timestamps, and metric windows aligned?
[ ] Are long-lag metrics mature?
[ ] Did schemas, metric definitions, or pipelines change during the experiment?
[ ] Can another analyst reproduce the scorecard from documented tables and filters?
[ ] Which metrics are reliable?
[ ] Which metrics are unreliable?
[ ] What severity label applies?
```

---

## 21. Integration with Other Playbooks

This playbook should run before:

- `ab_testing.md`
- `ads_experiments.md`
- `launch_decision.md`
- `did_policy_analysis.md`
- `guardrail_metrics.md`

Reason:

- A/B testing needs valid assignment, exposure, and outcome telemetry.
- Ads experiments need trustworthy attribution and conversion windows.
- Launch decisions need reliable metrics and guardrails.
- DiD and quasi-experiments need stable measurement over time.
- Guardrail analysis needs consistent metric lineage.

If telemetry trust fails, downstream playbooks should not treat the experiment result as causal evidence.

Recommended handoff:

| Telemetry Status | Downstream Handoff |
|---|---|
| `clean` | Proceed to A/B or launch decision playbook |
| `minor_warning` | Proceed with explicit caveat |
| `metric_unreliable` | Proceed only with reliable metrics |
| `experiment_unreliable` | Use `do_not_trust_result` in launch decision |
| `pipeline_blocker` | Stop and repair data pipeline |

---

## 22. Example: Conversion Lift with Assignment SRM

### User Question

> Treatment increased conversion by 3%, but sample ratio is off. Can we launch?

### Good Agent Answer

Telemetry Status: `experiment_unreliable`.

Do not use the 3% lift as causal evidence. Assignment SRM indicates that treatment and control may not be comparable or may not be logged consistently. The next step is to diagnose whether the SRM comes from randomization, eligibility filtering, exposure logging, bot imbalance, identity mapping, or analysis joins. Launch decision should be blocked until the root cause is resolved and the experiment is rerun or reanalyzed from a valid assignment population.

### Bad Answer

> Conversion increased by 3%, so launch carefully.

This is bad because unresolved SRM invalidates the causal comparison.

---

## 23. Example: CTR Spike from Duplicate Click Logging

### User Question

> CTR increased 12%, but revenue and retention are flat. Is this a good result?

### Good Agent Answer

Telemetry Status: `metric_unreliable` for CTR.

Before interpreting the CTR lift as user preference, check click event duplication, denominator changes, accidental clicks, UI area shifts, bot traffic, and client retry behavior. If duplicate click logging is variant-specific, CTR should be excluded from launch evidence. Revenue and retention may still be analyzable if their telemetry lineage is clean and mature.

---

## 24. Example: Triggered Analysis for Search Experiment

### User Question

> We only analyzed users who searched. Treatment improved purchase conversion among searchers. Is this valid?

### Good Agent Answer

Telemetry Status depends on trigger validity.

If "searched" is defined before the treatment ranking is shown and logged symmetrically in control and treatment, triggered analysis may be valid and more sensitive. If the treatment changes the probability of searching or changes whether a user appears in the searcher population, then the triggered population is post-treatment selected. In that case, triggered analysis is invalid for causal launch evidence, and the agent should use ITT or redesign the trigger.

---

## 25. Example: Retention Metric Not Mature

### User Question

> We ran the experiment for two days and 7-day retention looks flat. Can we ignore retention?

### Good Agent Answer

Telemetry Status: `metric_unreliable` for 7-day retention due to immaturity.

A 7-day retention metric cannot be final after two days. The metric should be marked `not_mature_yet`. Fast metrics such as exposure, render success, latency, and early activation may be mature, but retention cannot support a launch decision yet unless the decision is explicitly low risk and retention is monitored post-launch.

---

## 26. Example: Pipeline Backfill Changed Results

### User Question

> The scorecard changed after a backfill. Which result should we trust?

### Good Agent Answer

Telemetry Status: `pipeline_blocker` until reproducibility is restored.

The agent should not choose whichever result looks more favorable. It should reconstruct the analysis recipe, compare raw event counts before and after the backfill, verify schema and metric versions, and rerun the scorecard from versioned tables. No launch decision should depend on a non-reproducible scorecard.

---

## 27. Final Rule

The agent should optimize for trustworthy evidence, not for confident interpretation.

If telemetry is clean, proceed to causal analysis.

If one metric is unreliable, exclude that metric and continue only if the decision does not depend on it.

If assignment, exposure, trigger, identity, or core logging is unreliable, do not trust the experiment result.

If the pipeline is broken, stop analysis and repair the pipeline.

The final rule is:

> **No trusted telemetry, no trusted experiment, no responsible decision.**

---

## References and Methodological Inspiration

This playbook is inspired by public experimentation-platform practices and methodological writing from large-scale online experimentation teams:

- Microsoft Research, ExP Platform: "Diagnosing Sample Ratio Mismatch in A/B Testing." https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/
- Microsoft Research, ExP Platform: "Data Quality: Fundamental Building Blocks for Trustworthy A/B Testing Analysis." https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/data-quality-fundamental-building-blocks-for-trustworthy-a-b-testing-analysis/
- Microsoft Research, ExP Platform: "Patterns of Trustworthy Experimentation: Post-Experiment Stage." https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/patterns-of-trustworthy-experimentation-post-experiment-stage/
- Microsoft Research, ExP Platform: "Alerting in Microsoft's Experimentation Platform." https://www.microsoft.com/en-us/research/articles/alerting-in-microsofts-experimentation-platform-exp/
- Airbnb Engineering: "Experiment Reporting Framework." https://nerds.airbnb.com/experiment-reporting-framework/
- Netflix Tech Blog: "It's All A/Bout Testing: The Netflix Experimentation Platform." https://techblog.netflix.com/2016/04/its-all-about-testing-netflix.html
- Netflix Tech Blog: "What is an A/B Test?" https://netflixtechblog.com/what-is-an-a-b-test-b08cc1b57962
- Netflix Research: "Experimentation and Causal Inference." https://research.netflix.com/research-area/experimentation-and-causal-inference
