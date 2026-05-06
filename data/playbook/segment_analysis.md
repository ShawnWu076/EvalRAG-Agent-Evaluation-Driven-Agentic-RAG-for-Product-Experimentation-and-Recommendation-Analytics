# Segment Analysis Playbook

This playbook defines how an Agent should reason about segment analysis in product experiments, marketplace experiments, ads experiments, policy analysis, and launch decisions.

It is designed for an evaluation-driven Agentic RAG system. The goal is not to make the Agent slice every experiment by every possible user attribute. The goal is to make the Agent behave like a senior data scientist who can identify heterogeneous treatment effects, protect strategically important groups from hidden harm, avoid false discoveries, and translate segment evidence into responsible rollout decisions.

Segment analysis should make launch decisions safer and more precise, not noisier and more cherry-picked.

A good segment analysis balances two risks:

1. **Average-effect blindness**: the overall experiment result hides meaningful benefit or harm in important segments.
2. **Segment p-hacking**: the analyst searches many segments after seeing the result and over-interprets noisy or false-positive patterns.

The Agent should not say “segment A is significant, so launch there” unless the segment result is valid, powered, decision-relevant, and consistent with the product hypothesis.

---

## Quick Retrieval Summary

Use this playbook when the user asks about:

- heterogeneous treatment effects;
- segment-level experiment results;
- whether an experiment works for some users but not others;
- whether a positive average effect hides harm in a subgroup;
- whether a feature should launch only to a segment;
- new users vs existing users;
- power users vs casual users;
- buyer/seller/creator/advertiser cohorts;
- geography, platform, device, app version, traffic source, or market-level differences;
- whether a segment result is trustworthy;
- whether segment analysis is p-hacking;
- whether a segment finding should affect launch.

This playbook is especially relevant when:

- the overall result is positive but a key segment is negative;
- the overall result is neutral but one segment looks strongly positive;
- a guardrail harm is concentrated in one group;
- the user asks for targeted rollout;
- the feature is intended for a specific audience;
- the experiment involves marketplace sides, advertisers, creators, sellers, or policy-sensitive groups;
- many segment cuts were inspected after the fact;
- segment sample sizes are small or confidence intervals are wide;
- segment variables may be affected by treatment;
- segment composition differs across treatment and control.

Default reasoning order:

1. Clarify the decision problem.
2. Define the overall metric hierarchy.
3. Classify segments as pre-specified or exploratory.
4. Check whether segment variables are valid pre-treatment covariates.
5. Check segment-level balance, SRM, missingness, and telemetry reliability.
6. Estimate segment effects with uncertainty.
7. Test treatment-by-segment interaction when possible.
8. Account for multiple testing and power.
9. Separate harm scan from opportunity scan.
10. Translate segment evidence into a rollout, investigation, or launch-block decision.

---

## 1. Core Principle

Segment analysis should protect decision quality from average-effect blindness without becoming p-hacking.

The Agent should use segment analysis to answer four questions:

1. **Consistency**: Is the treatment effect directionally consistent across important groups?
2. **Hidden harm**: Does the average effect hide harm to a strategically important segment?
3. **Targeting opportunity**: Is the benefit concentrated enough to justify targeted rollout?
4. **Mechanism**: Do segment differences explain why the treatment works or fails?

The Agent should not use segment analysis to:

- rescue a failed experiment by searching for a positive subgroup;
- ignore the pre-specified decision metric;
- treat noisy exploratory cuts as confirmatory evidence;
- compare “significant in one segment” with “not significant in another segment” as proof of heterogeneity;
- use post-treatment variables as causal segment definitions;
- recommend broad launch when a key segment is harmed beyond tolerance.

---

## 2. Segment Analysis Goals

Segment analysis has different goals depending on the decision context.

### 2.1 Safety and Harm Detection

Use segment analysis to detect whether a product change harms important groups.

Examples:

- existing users lose retention while new users gain activation;
- high-value customers churn while low-value users click more;
- sellers in sparse markets lose exposure;
- small advertisers lose ROI while large advertisers gain scale;
- creators in a long-tail cohort lose distribution;
- users on older devices experience latency or crash regressions.

Harm detection is often more important than opportunity discovery because it protects against broad launches that damage durable product value.

### 2.2 Targeted Rollout

Use segment analysis to decide whether a feature should launch only to a subset.

A targeted rollout is appropriate only when:

- segment benefit is meaningful;
- the segment is business-relevant;
- the segment definition is available before treatment;
- guardrails pass inside the target segment;
- harmed segments can be excluded cleanly;
- the implementation can target the segment without creating fairness, policy, or operational risk.

### 2.3 Mechanism Diagnosis

Use segment analysis to understand why the treatment effect occurred.

Examples:

- a checkout change works only for mobile users, suggesting UI friction;
- a recommendation change works only for new users, suggesting discovery improvement;
- an ads change works only for high-intent users, suggesting attribution or auction-quality effects;
- a marketplace ranking change works only in dense markets, suggesting supply availability constraints.

Mechanism segment analysis can guide product iteration, even when it does not justify launch by itself.

### 2.4 Personalization and Heterogeneous Policy

Use segment analysis to decide whether a personalized policy may outperform a global launch.

The Agent should be conservative: personalization requires evidence that the value of differentiated treatment exceeds the complexity, maintenance cost, fairness risk, and monitoring burden.

---

## 3. Segment Evidence Labels

Every segment finding should receive one evidence label.

### 3.1 `pre_specified_confirmatory`

Use when the segment was specified before the experiment as part of the decision rule.

Requirements:

- segment definition pre-specified;
- metric and direction pre-specified;
- adequate sample size or planned power;
- valid pre-treatment segment variable;
- interaction or segment contrast supports heterogeneity;
- multiple testing handled if more than one segment was confirmatory.

Decision weight:

- can influence launch decision directly.

### 3.2 `pre_specified_diagnostic`

Use when the segment was specified before the experiment for monitoring or diagnosis, but not as a primary decision rule.

Decision weight:

- can support interpretation;
- can trigger investigation or monitoring;
- should not override the OEC unless harm is material.

### 3.3 `exploratory_hypothesis`

Use when the segment was discovered after viewing results or was not part of the pre-specified plan.

Decision weight:

- hypothesis-generating only;
- can justify follow-up experiment, targeted holdout, or deeper analysis;
- should not be used alone to justify launch.

### 3.4 `harm_signal`

Use when a segment shows possible material harm, even if exploratory.

Decision weight:

- should trigger caution, especially for strategic, protected, high-value, safety-sensitive, or ecosystem-critical groups;
- may block broad launch if harm is large, credible, and decision-relevant.

### 3.5 `unreliable_noise`

Use when the segment estimate is too small, underpowered, imbalanced, post-treatment, or inconsistent to support a conclusion.

Decision weight:

- should not drive launch;
- may be logged for future monitoring.

### 3.6 `invalid_segment`

Use when the segment variable, population, or telemetry is not valid for causal interpretation.

Examples:

- segment defined using post-treatment behavior;
- segment assignment differs by treatment;
- segment-level SRM is unresolved;
- segment filter drops users differently across variants;
- missingness differs by segment and variant;
- segment identity is unstable.

Decision weight:

- do not use as causal evidence.

---

## 4. Segment Taxonomy

The Agent should select segments based on product logic, risk, and decision relevance.

### 4.1 User Lifecycle Segments

Examples:

- new users;
- existing users;
- resurrected users;
- power users;
- casual users;
- dormant users;
- recently activated users;
- long-tenured users.

Use when the feature may affect learning, habituation, retention, or onboarding.

### 4.2 Value and Engagement Segments

Examples:

- high-value vs low-value users;
- paid vs free users;
- high-LTV cohort;
- frequent purchasers;
- high-intent users;
- low-intent browsers;
- subscribers vs non-subscribers.

Use when the business impact differs by user value or intent.

### 4.3 Platform and Technical Segments

Examples:

- iOS vs Android;
- web vs mobile;
- app version;
- browser;
- device class;
- network quality;
- logged-in vs logged-out users.

Use when the treatment may create technical or UX regressions.

### 4.4 Acquisition and Traffic Source Segments

Examples:

- organic traffic;
- paid acquisition;
- referral;
- email;
- push notification;
- SEO;
- direct traffic;
- retargeting traffic.

Use when user intent or attribution quality differs by channel.

### 4.5 Geography and Market Segments

Examples:

- country;
- region;
- city;
- dense vs sparse market;
- mature vs new market;
- language;
- regulatory market.

Use when localization, supply density, regulation, or cultural context matters.

### 4.6 Marketplace-Side Segments

Examples:

- buyers;
- sellers;
- providers;
- hosts;
- drivers;
- creators;
- advertisers;
- agencies;
- long-tail sellers;
- top sellers;
- new sellers;
- mature sellers;
- sparse-market supply.

Use when one side of a marketplace may benefit while another side pays the cost.

### 4.7 Ads and Auction Segments

Examples:

- small vs large advertisers;
- high-spend vs low-spend advertisers;
- new advertisers;
- retained advertisers;
- high-intent users;
- ad-sensitive users;
- auction density buckets;
- campaign objective;
- vertical;
- bid strategy.

Use when short-term platform revenue may trade off against advertiser ROI or user experience.

### 4.8 Content and Recommendation Segments

Examples:

- content category;
- creator tier;
- viewer intent;
- freshness bucket;
- quality tier;
- safety risk tier;
- language;
- content maturity.

Use when ranking, discovery, or content allocation may change ecosystem incentives.

### 4.9 Policy and Safety Segments

Examples:

- risk tier;
- moderation history;
- age-sensitive groups;
- compliance-relevant geography;
- appeal status;
- trust level;
- enforcement cohort.

Use when fairness, safety, policy, or irreversible harm is possible.

---

## 5. Metric Hierarchy Before Segmenting

The Agent must define the overall metric hierarchy before interpreting segment results.

Segment analysis should be anchored to:

- OEC / decision metric;
- success metrics;
- guardrail metrics;
- diagnostic metrics;
- long-term proxy metrics;
- business metrics;
- trust/safety metrics.

Bad reasoning:

> Android CTR is significant, so the feature works.

Better reasoning:

> CTR is diagnostic. The decision metric is 7-day retention and the guardrails are latency and crash rate. Android CTR lift is not enough to justify rollout unless durable metrics and technical guardrails pass.

Agent Action:

- If segment results are reported only for diagnostic metrics, require decision-metric and guardrail readouts before launch.
- If a strategic guardrail is harmed in a segment, treat it as decision-relevant even if the OEC improves overall.
- If segment benefit is on a shallow metric but harm is on durable value, prioritize durable value.

---

## 6. Pre-Specified vs Exploratory Segments

The Agent must distinguish confirmatory evidence from exploratory evidence.

### 6.1 Pre-Specified Segment Analysis

A segment is pre-specified if the experiment plan defined before launch:

- segment variable;
- segment definition;
- metric;
- expected direction;
- minimum sample size or power;
- decision rule;
- multiple testing approach;
- whether the segment can drive rollout.

Pre-specified segments can carry decision weight.

### 6.2 Exploratory Segment Mining

Exploratory segment mining is useful for learning, but dangerous for decision-making.

Exploratory segment findings are weaker because:

- many cuts increase false positives;
- small samples produce noisy effects;
- analysts may cherry-pick favorable findings;
- segment definitions may be tuned after seeing results;
- effect may not replicate.

Agent Action:

- Label exploratory segment results as `exploratory_hypothesis`.
- Do not recommend launch solely from exploratory segment lift.
- Recommend follow-up test, targeted validation, or holdout if the segment is promising.
- Treat exploratory harm signals seriously enough to investigate, especially for strategic or safety-sensitive segments.

---

## 7. Interaction Test First

The Agent should not infer heterogeneity only because one segment is statistically significant and another is not.

Bad reasoning:

> The treatment is significant for new users but not significant for existing users, so the effect is different.

Better reasoning:

> Test whether the treatment effect differs between new and existing users using a treatment-by-segment interaction or a direct contrast between segment effects.

Preferred approaches:

- regression with treatment, segment, and treatment × segment interaction;
- direct difference-in-differences across segments within the randomized experiment;
- hierarchical or shrinkage models for many segments;
- causal forest or HTE methods for exploratory discovery;
- CATE estimation with validation for personalization decisions.

Agent Action:

- When feasible, report whether the interaction is credible.
- If interaction evidence is unavailable, state that apparent segment differences are provisional.
- Do not compare p-values across segments as evidence of heterogeneity.

---

## 8. Multiple Testing and False Discovery Control

Every additional segment cut increases the chance of false positives.

The Agent must ask:

- How many segment cuts were inspected?
- Were the segments pre-specified?
- Were metrics pre-specified?
- Were all segment results reported, or only the interesting ones?
- Was correction applied?
- Was FDR controlled?
- Are confidence intervals adjusted?
- Is the finding replicated across time or experiments?

Possible approaches:

- Bonferroni correction for strict family-wise error control;
- Holm correction;
- Benjamini-Hochberg false discovery rate control;
- hierarchical modeling or empirical Bayes shrinkage;
- holdout validation;
- follow-up confirmatory experiment.

Agent Action:

- If many segments were mined and no correction was applied, downgrade the evidence.
- Treat the segment as hypothesis-generating unless the result is large, plausible, replicated, and decision-critical.
- Do not hide the number of tested segments.

---

## 9. Power, Sample Size, and Business Weight

A segment effect is not useful if it is too noisy or too small to matter.

For each important segment, the Agent should report:

- sample size;
- traffic share;
- revenue or business share;
- baseline metric value;
- effect estimate;
- confidence interval;
- minimum detectable effect if available;
- whether the segment is powered;
- whether the effect is practically meaningful;
- whether the segment is strategically important.

Agent Action:

- If the segment is underpowered, label the result as `inconclusive_segment`.
- If the confidence interval includes meaningful harm, do not claim the segment is safe.
- If the segment is small but strategically important, treat uncertainty as a reason for cautious rollout or follow-up testing.
- If the segment is large but effect is tiny, consider practical magnitude before recommending targeting.

### 9.1 Noise Reduction via Shrinkage Estimation

A top data scientist avoids "extremism" in segment analysis. When an experiment has many segments (e.g., 50 countries), the segments with the smallest sample sizes will naturally show the most extreme (positive or negative) results due to variance.

- **The Problem:** The "winner" in an exploratory segment scan is often just the segment with the most noise.
- **The Solution (Empirical Bayes Shrinkage):** "Shrink" segment-level estimates toward the aggregate (global) average. 
    - The formula for a shrunken estimate $\hat{\theta}_{shrunken}$ is roughly:
      $$\hat{\theta}_{i, shrunken} = w_i \hat{\theta}_i + (1 - w_i) \hat{\theta}_{global}$$
    - Where $w_i$ is determined by the precision (inverse variance) of the segment's data. 
- **Agent Action:** - If a small segment shows a massive lift, calculate the shrunken estimate before recommending it as a targeting opportunity.
    - Be skeptical of "outlier segments" that have low volume and high variance.

---

## 10. Harm Scan vs Opportunity Scan

The Agent should separate two different workflows.

### 10.1 Harm Scan

Goal:

- detect whether the treatment harms important users, sellers, creators, advertisers, markets, or policy-sensitive groups.

Harm scan should prioritize:

- strategic users;
- high-value users;
- vulnerable or safety-sensitive groups;
- key supply-side groups;
- high-risk geographies;
- high-retention cohorts;
- ecosystem-critical groups.
- **Fairness & Bias Audit:** - Beyond business metrics, scan for "Equity Guardrails." 
    - Does the treatment perform significantly worse for segments defined by socio-economic proxies or sensitive attributes (e.g., older devices, low-bandwidth regions, minority languages)?
    - A top data scientist flags "disparate impact" even if the aggregate OEC is positive, as this represents a long-term trust and regulatory risk.

A harm signal can matter even if exploratory, especially when:

- effect size is large;
- guardrail harm exceeds tolerance;
- group is strategically important;
- harm is plausible given product mechanism;
- similar harm appears across related metrics.

### 10.2 Opportunity Scan

Goal:

- identify where treatment benefit is concentrated and whether targeted rollout is justified.

Opportunity scan requires stronger evidence than harm scan because it is often more vulnerable to p-hacking.

Agent Action:

- Use harm scan to protect launch safety.
- Use opportunity scan to generate targeting hypotheses.
- Require validation before recommending segment-specific launch from exploratory opportunity signals.

---

## 11. Segment Validity Checks

Before interpreting segment effects, the Agent must check whether the segment definition is causally valid.

### 11.1 Pre-Treatment Segment Requirement

Valid segment variables should usually be measured before treatment assignment.

Examples of valid pre-treatment segments:

- country at assignment;
- platform at assignment;
- prior activity tier;
- prior purchase status;
- prior seller cohort;
- pre-experiment advertiser spend tier;
- pre-experiment market density.

Examples of risky post-treatment segments:

- users who clicked after treatment;
- users who completed onboarding after treatment;
- users with high engagement during the experiment;
- sellers who received high exposure after treatment;
- users who saw a specific treatment-induced module.

Agent Action:

- If the segment is post-treatment, mark it as `invalid_segment` for causal interpretation unless explicitly framed as mechanism analysis.
- If the segment may be treatment-induced, do not use it to recommend launch.

### 11.2 Segment-Level SRM and Composition Balance

The Agent must check whether segment composition is balanced across variants.

Checks:

- treatment/control counts within each segment;
- segment share by variant;
- missing segment labels by variant;
- segment-level SRM;
- platform/version/geography imbalance within segment;
- pre-treatment metric balance within segment.

Agent Action:

- If segment-level SRM is present, use `sample_ratio_mismatch.md`.
- If missing labels differ by variant, use `experiment_telemetry.md`.
- Do not interpret segment effects until the imbalance is diagnosed.

### 11.3 Telemetry Reliability

Segment analysis depends on reliable logging.

Check:

- whether the segment label is consistently logged;
- whether it is derived from stable identity;
- whether it changes during the experiment;
- whether it is affected by privacy settings;
- whether it is missing differentially by treatment;
- whether metric logging differs across segment and variant.

---

## 12. Simpson’s Paradox and Composition Shift

Aggregate effects can reverse or distort segment effects when composition differs.

The Agent should check:

- whether treatment/control segment composition is balanced;
- whether overall lift is driven by segment mix;
- whether within-segment effects differ from aggregate effect;
- whether a large segment dominates the overall estimate;
- whether segment weights should be standardized;
- whether local-market or cohort composition changed during ramp.

Agent Action:

- If aggregate effect differs from all segment effects, investigate composition shift.
- If treatment has more high-baseline users in one variant, do not treat aggregate lift as causal until balance is verified.
- If segment shares differ due to treatment-induced filtering, treat segment result as invalid for causal launch decisions.

### 12.1 Inter-segment Interference (Cannibalization)

In marketplaces or social ecosystems, a lift in one segment may come at the direct expense of another (Zero-sum dynamics).

- **Segment Cannibalization:** A ranking change that helps "Power Users" find deals faster might cannibalize the inventory available for "New Users," leading to long-term ecosystem harm.
- **Agent Action:** - Check if the gains in the "Winning Segment" are mathematically offset by losses in other segments.
    - In marketplace contexts, always pair "Buyer Segment Analysis" with "Seller Segment Analysis" to ensure the treatment isn't just shifting value from one group to another without creating net platform incrementality.

---

## 13. Temporal Segment Analysis

Segment effects can change over time.

The Agent should check:

- date-level segment effects;
- days-since-exposure;
- novelty effects;
- primacy effects;
- learning effects;
- fatigue effects;
- weekday/weekend differences;
- ramp-stage differences;
- event or seasonality shocks.

Examples:

- new users show a first-day activation lift that disappears by day 7;
- existing users initially dislike a UI change but adapt after one week;
- push notifications increase short-term sessions but produce fatigue in week 2;
- marketplace subsidies lift transactions during a holiday period but not after.

Agent Action:

- Do not recommend launch from a short-lived segment spike.
- If segment effect decays rapidly, classify as novelty/fatigue risk.
- If segment effect strengthens over time, consider primacy or learning effects.
- For durable decisions, require readouts at appropriate maturity windows.

---

## 14. Segment-Based Rollout Rules

The Agent should convert segment evidence into one decision label.

Allowed labels:

- `consistent_effect`
- `targeted_rollout`
- `partial_rollout`
- `investigate_further`
- `do_not_launch`
- `do_not_use_segment_result`

### 14.1 `consistent_effect`

Use when:

- segment effects broadly align with the overall result;
- no important segment is harmed;
- uncertainty is acceptable;
- guardrails pass across segments.

Decision implication:

- segment analysis does not block overall launch.

### 14.2 `targeted_rollout`

Use when:

- benefit is concentrated in a valid, pre-treatment, business-relevant segment;
- segment effect is meaningful and credible;
- guardrails pass in the target segment;
- non-target segments are neutral or harmed;
- the product can reliably target the segment;
- fairness and operational risks are acceptable.
- **Complexity Tax Assessment:** - A top scientist asks: "Is the lift in this segment large enough to justify maintaining a separate code path/model for this group?"
    - Every targeted rollout adds technical debt, fragmentation in user experience, and increased monitoring burden.
    - If the incremental gain from targeting Segment A vs. a global launch is marginal (e.g., < 5% of the total lift), prefer the simpler global launch to avoid the "complexity tax."

The Agent must specify:

- target segment;
- inclusion rule;
- excluded segments;
- monitoring metrics;
- expansion criteria;
- rollback threshold.

### 14.3 `partial_rollout`

Use when:

- segment evidence is promising but not strong enough for permanent targeting;
- harm risk exists in some segments;
- more data is needed before broad launch;
- targeted rollout should be limited in scale or time.

The Agent must specify:

- rollout size;
- target population;
- duration;
- monitoring plan;
- decision threshold.

### 14.4 `investigate_further`

Use when:

- segment results conflict;
- interaction evidence is unclear;
- confidence intervals are wide;
- multiple testing risk is high;
- segment variable validity is uncertain;
- guardrail harm needs diagnosis;
- mechanism is unclear.

### 14.5 `do_not_launch`

Use when:

- a strategic segment is harmed beyond tolerance;
- harm appears on durable value or safety metrics;
- broad launch would expose a harmed group;
- targeted exclusion is not feasible;
- fairness, trust, policy, or ecosystem risk is material.

### 14.6 `do_not_use_segment_result`

Use when:

- segment is post-treatment;
- segment-level SRM is unresolved;
- segment label missingness differs by variant;
- many exploratory cuts were cherry-picked;
- sample is too small to support inference;
- telemetry is unreliable.

---

## 15. Segment Decision Matrix

| Evidence Pattern | Recommended Decision |
|---|---|
| Overall positive, all key segments positive or neutral, guardrails pass | `consistent_effect` |
| Benefit concentrated in pre-specified, powered, valid segment | `targeted_rollout` |
| Benefit concentrated in exploratory segment only | `investigate_further` or `partial_rollout` |
| Overall positive but high-value segment harmed | `partial_rollout` or `do_not_launch` |
| Overall positive but safety-sensitive group harmed | usually `do_not_launch` or `investigate_further` |
| Overall neutral but one exploratory segment positive among many cuts | `investigate_further` |
| Segment effect based on post-treatment behavior | `do_not_use_segment_result` |
| Segment-level SRM or logging imbalance detected | `do_not_use_segment_result` until diagnosed |
| Segment sample small and CI wide | `investigate_further` |
| Interaction test supports heterogeneity and guardrails pass | `targeted_rollout` or `partial_rollout` |
| Significant in one segment, non-significant in another, no interaction test | `investigate_further` |
| Short-term segment lift decays over time | `investigate_further` or `partial_rollout` |
| Segment guardrail harm exceeds tolerance | `do_not_launch` or restrict rollout |

---

## 16. Scenario Playbooks

### 16.1 New Users Improve, Existing Users Decline

Agent should ask:

- Was new-user improvement the intended hypothesis?
- Is existing-user decline on a decision metric or guardrail?
- Are existing users high-value or strategically important?
- Can the feature be shown only to new users?
- Is the existing-user decline temporary adaptation or persistent harm?
- Are retention, complaints, support tickets, and revenue stable?

Likely decision:

- `targeted_rollout` to new users if evidence is strong and existing users can be excluded.
- `investigate_further` if the existing-user decline may be temporary or noisy.
- `do_not_launch` if existing-user harm is material and targeting is infeasible.

### 16.2 Android Positive, iOS Neutral or Negative

Agent should ask:

- Is the treatment technically different across platforms?
- Are app versions balanced?
- Is there platform-level SRM?
- Are latency, crash rate, and render success stable?
- Is the platform segment pre-specified?
- Is the interaction credible?

Likely decision:

- `targeted_rollout` only if Android benefit is credible and iOS harm is avoided.
- `investigate_further` if platform telemetry or version imbalance may explain the result.

### 16.3 Marketplace Buyer Conversion Up, Seller Metrics Down

Agent should ask:

- Which seller cohorts are harmed?
- Are long-tail sellers losing exposure?
- Are seller earnings or retention affected?
- Did ranking concentrate demand among top sellers?
- Is seller-side harm a guardrail breach?

Likely decision:

- `partial_rollout`, `investigate_further`, or `do_not_launch`.

Also use `marketplace_metrics.md`.

### 16.4 Ads Revenue Up, Small Advertiser ROI Down

Agent should ask:

- Are small advertisers strategically important for auction density?
- Is platform revenue coming from lower advertiser efficiency?
- Are advertiser retention and spend quality stable?
- Is ROI decline beyond tolerance?
- Is the effect concentrated by advertiser size, vertical, bid strategy, or campaign goal?

Likely decision:

- `investigate_further` or `do_not_launch` if small advertiser harm is material.

Also use `ads_experiments.md`.

### 16.5 Exploratory Segment Looks Very Positive

Agent should ask:

- How many segments were inspected?
- Was this segment pre-specified?
- Is the segment sample large enough?
- Is the effect plausible given mechanism?
- Is there an interaction test?
- Does the result replicate across time?
- Are guardrails stable?

Likely decision:

- `investigate_further`.
- Consider follow-up targeted experiment.

### 16.6 Segment Harm on Guardrail Metric

Agent should ask:

- Is the guardrail strategically important?
- Does harm exceed non-inferiority tolerance?
- Is harm concentrated in high-value or vulnerable groups?
- Is the guardrail mature enough?
- Can rollout exclude the harmed segment?

Likely decision:

- `partial_rollout` or `do_not_launch`.

### 16.7 Segment Defined by Post-Treatment Behavior

Example:

> The treatment works well among users who clicked the new module.

Agent should respond:

- This segment is post-treatment and cannot be used as causal segment evidence.
- It may be useful for mechanism analysis but not launch targeting.
- Use ITT or pre-treatment segments, or redesign the experiment.

Likely decision:

- `do_not_use_segment_result`.

---

## 17. Worked Decision Examples

### Example 1: Overall Positive, Strategic Segment Harmed

Input:

- Overall activation: +1.8%, statistically significant.
- New users: +4.2%.
- Existing high-value users: 7-day retention -0.6 percentage points.
- Pre-defined retention guardrail tolerance: -0.2 percentage points.
- Segment was pre-specified.

Decision:

- `partial_rollout` or `do_not_launch`.

Reason:

- The average activation gain hides guardrail harm in a strategic segment. Broad launch is not justified. If technically feasible, restrict to new users and monitor existing-user retention.

### Example 2: Exploratory Android Lift

Input:

- Overall conversion: flat.
- Android conversion: +3.5%, p < 0.05.
- iOS conversion: +0.2%.
- 28 exploratory segments inspected.
- No multiple testing correction.
- No interaction test.

Decision:

- `investigate_further`.

Reason:

- The Android result is hypothesis-generating. It should not justify Android-only launch without validation, interaction evidence, and correction for multiple testing.

### Example 3: Segment Based on Clickers

Input:

- Treatment works among users who clicked the new module.
- Click is affected by treatment.

Decision:

- `do_not_use_segment_result`.

Reason:

- The segment is post-treatment. It may explain mechanism, but it cannot be used as causal evidence for targeting or launch.

### Example 4: Marketplace Dense Markets Only

Input:

- Search-to-book improves in dense markets.
- Sparse markets show higher no-availability rate.
- Seller earnings stable in dense markets but decline in sparse markets.

Decision:

- `targeted_rollout` or `partial_rollout` to dense markets only.

Reason:

- Benefit is local-market-specific. Broad rollout would harm sparse-market supply-side health.

---

## 18. Required Output for Segment Analysis

A complete Agent response should include:

### 18.1 Decision Summary

- decision label;
- whether segment evidence supports broad launch, targeted rollout, or investigation;
- main segment risk.

### 18.2 Overall Effect

- OEC result;
- success metric result;
- guardrail result;
- uncertainty.

### 18.3 Segment Plan

- pre-specified segments;
- exploratory segments;
- strategic/protected segments;
- harm-scan segments;
- opportunity-scan segments.

### 18.4 Segment Results Table

Include for each key segment:

- segment name;
- sample size;
- traffic share;
- business share if available;
- effect estimate;
- confidence interval;
- guardrail status;
- interaction evidence;
- reliability;
- decision impact.

### 18.5 Validity Checks

- pre-treatment segment variable;
- segment-level SRM;
- missingness by variant;
- telemetry consistency;
- multiple testing handling;
- power and MDE;
- post-treatment selection risk.

### 18.6 Recommendation

- launch, targeted rollout, partial rollout, investigate, do not launch, or do not use segment result;
- missing evidence;
- next experiment or analysis;
- monitoring plan;
- rollback thresholds.

---

## 19. Agent Response Template

Use this structure when answering a segment analysis question.

```text
Decision:
[consistent_effect / targeted_rollout / partial_rollout / investigate_further / do_not_launch / do_not_use_segment_result]

Decision problem:
[Restate the product or experiment decision.]

Overall metric hierarchy:
- OEC / decision metric:
- Success metrics:
- Guardrail metrics:
- Diagnostic metrics:

Overall effect:
[Estimate, uncertainty, practical significance.]

Segment evidence status:
[pre_specified_confirmatory / pre_specified_diagnostic / exploratory_hypothesis / harm_signal / unreliable_noise / invalid_segment]

Segment plan:
- Pre-specified segments:
- Exploratory segments:
- Strategic / protected segments:
- Harm scan:
- Opportunity scan:

Segment results:
| Segment | n | Traffic/business share | Effect | CI | Guardrail status | Interaction evidence | Reliability | Decision impact |
|---|---:|---:|---:|---:|---|---|---|---|

Validity checks:
- Segment variable pre-treatment:
- Segment-level SRM:
- Missingness/logging:
- Post-treatment selection risk:
- Multiple testing:
- Power / MDE:
- Temporal stability:

Interpretation:
[What the segment evidence does and does not prove.]

Recommendation:
[Clear action.]

Missing evidence:
- [Evidence 1]
- [Evidence 2]
- [Evidence 3]

Next steps:
- [Follow-up analysis or validation]
- [Targeted rollout / holdout / rerun plan]
- [Monitoring and rollback thresholds]
```

---

## 20. Evaluation Criteria for Agent Answers

A high-quality Agent answer should:

- define the overall metric hierarchy before interpreting segments;
- distinguish pre-specified and exploratory segments;
- identify whether segment variables are pre-treatment;
- check segment-level SRM and telemetry reliability;
- report sample size, business share, effect size, and uncertainty;
- avoid comparing p-values across segments;
- request or use treatment-by-segment interaction evidence;
- account for multiple testing;
- distinguish harm scan from opportunity scan;
- treat strategic segment harm seriously;
- avoid broad launch when key segments are harmed;
- recommend targeted rollout only when segment evidence is credible and implementable;
- state missing evidence and next steps;
- choose exactly one decision label.

Penalize an answer if it:

- says one segment is significant and another is not, therefore heterogeneity exists;
- cherry-picks a positive exploratory segment;
- ignores multiple testing;
- ignores small segment sample size;
- ignores segment-level SRM;
- uses post-treatment behavior as a causal segment;
- recommends broad launch despite harm in a strategic segment;
- treats diagnostic metric lift as enough for segment rollout;
- gives generic advice without a decision label;
- recommends targeted rollout without specifying target definition, monitoring, and rollback criteria.

---

## 21. Common Failure Modes

The Agent should avoid these failure modes:

1. **Average-effect blindness**

   Launching because the overall effect is positive while ignoring harmed key segments.

2. **Segment p-hacking**

   Searching many segments and reporting only favorable results.

3. **P-value comparison fallacy**

   Claiming heterogeneity because one segment is significant and another is not.

4. **Underpowered segment inference**

   Over-interpreting small segment samples with wide confidence intervals.

5. **Post-treatment segmentation**

   Defining segments using behavior caused by the treatment.

6. **Ignoring multiple testing**

   Treating exploratory segment cuts as confirmatory evidence.

7. **Ignoring segment telemetry**

   Failing to check missingness, SRM, or logging reliability by segment.

8. **Diagnostic metric targeting**

   Targeting based on CTR, clicks, or impressions without checking decision metrics and guardrails.

9. **No business relevance**

   Highlighting statistically interesting but strategically irrelevant segments.

10. **Overconfident targeting**

   Recommending permanent segment-specific launch from one noisy experiment.

---

## 22. Integration with Other Playbooks

Use related playbooks when segment analysis reveals cross-cutting risks.

- Use `sample_ratio_mismatch.md` when segment-level sample ratios are imbalanced.
- Use `experiment_telemetry.md` when segment labels, exposure, or metric logging may be unreliable.
- Use `ab_testing.md` for core randomized experiment interpretation.
- Use `launch_decision.md` when segment evidence affects launch recommendation.
- Use `ads_experiments.md` when user/advertiser/auction segments are involved.
- Use `marketplace_metrics.md` when buyer/seller/creator/provider segments are involved.
- Use `did_policy_analysis.md` when segment heterogeneity comes from policy rollout, staggered adoption, or observational causal analysis.

---

## 23. External Methodology References

These references are included to help future maintainers understand the methodological background behind this playbook.

- ICH E9, "Statistical Principles for Clinical Trials." Relevant for pre-specified subgroup analysis, cautious interpretation of exploratory subgroup findings, and interaction analysis principles.
- EMA, "Guideline on the Investigation of Subgroups in Confirmatory Clinical Trials."
- Wang et al., "Statistical Considerations for Subgroup Analyses."
- Benjamini and Hochberg, "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing."
- Netflix Tech Blog, "Heterogeneous Treatment Effects at Netflix."
- Netflix Research, "Treatment Effect Risk: Bounds and Inference."
- Netflix `sherlock`, "Causal Machine Learning for Segment Discovery."
- Microsoft ExP, "Patterns of Trustworthy Experimentation: During-Experiment Stage."
- Deng, "Statistical Analysis of A/B Tests," especially discussion of multiple testing.

---

## 24. Final Rule

Segment analysis should make product decisions safer, more precise, and more honest.

The Agent should use segments to detect hidden harm, understand mechanisms, and identify credible targeted rollout opportunities. It should not use segments to manufacture significance.

If a segment result is exploratory, underpowered, post-treatment, imbalanced, or cherry-picked, the Agent must not treat it as confirmatory launch evidence.

If an important segment is credibly harmed, the Agent must not recommend broad launch just because the average effect is positive.

The best segment analysis answer should feel like a senior data scientist protecting decision quality, not like a dashboard slicing metrics until something looks significant.
