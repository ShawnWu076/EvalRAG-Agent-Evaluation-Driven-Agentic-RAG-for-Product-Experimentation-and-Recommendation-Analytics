# Ads Experiments Playbook

This playbook defines how an agent should design, audit, analyze, and make decisions from advertising experiments.

It is written for an evaluation-driven Agentic RAG system. The goal is not to explain basic A/B testing, CTR, or conversion rate. The goal is to make the agent behave like a senior data scientist working across ads measurement, attribution, incrementality, auction dynamics, user experience, advertiser value, and long-term marketplace health.

A good ads experiment answer should make clear:

- what advertising decision is being made;
- whether the evidence is experimental, quasi-experimental, or observational;
- whether the result measures attribution, incrementality, auction effect, user-learning effect, or marketplace total effect;
- whether the experiment design matches the causal question;
- whether auction dynamics, budgets, pacing, or marketplace interference bias the readout;
- whether revenue gains are durable or borrowed from users, advertisers, or future platform health;
- whether the metric hierarchy protects users, advertisers, and the platform;
- what validity checks were performed before interpreting lift;
- what anomalies, fraud, latency, filtering bias, or outliers could explain the result;
- what decision label is justified;
- and what the next responsible action should be.

The agent should not recommend launch because CTR, attributed conversions, or short-term ad revenue increased. It should first ask whether the movement is causal, incremental, economically meaningful, and safe for users and advertisers.

The correct ads experiment decision is **incrementality-aware, auction-aware, user-aware, advertiser-aware, and auditable**.

---

## Quick Retrieval Summary

Use this playbook when the user asks about:

- ad campaign lift;
- conversion lift;
- incrementality testing;
- ROAS, iROAS, CPA, CAC, LTV, or payback;
- ad ranking experiments;
- auction mechanism changes;
- ad load, ad density, ad frequency, or ad placement changes;
- targeting, retargeting, lookalike, or audience expansion experiments;
- bidding, pacing, budget allocation, or optimization experiments;
- advertiser ROI, advertiser retention, or advertiser value;
- user experience tradeoffs caused by ads;
- ads marketplace interference;
- geo experiments, switchback tests, cluster randomization, Ghost Ads, PSA tests, or holdout tests;
- observational attribution versus causal measurement;
- suspicious CTR or conversion spikes;
- bot traffic, click fraud, accidental clicks, low-quality conversions, or abnormal large orders;
- whether short-term ad revenue gains are sustainable.

Default reasoning order:

1. Clarify the ads decision.
2. Identify whether the question is about advertiser effectiveness, platform monetization, user experience, or marketplace health.
3. Classify the causal estimand: attributed effect, incremental effect, auction effect, user-learning effect, advertiser-retention effect, or marketplace total effect.
4. Choose the correct experiment design.
5. Validate experiment trustworthiness before interpreting lift.
6. Define the metric hierarchy.
7. Evaluate incrementality and value quality.
8. Evaluate auction dynamics and interference.
9. Evaluate user, advertiser, and platform guardrails.
10. Analyze segment heterogeneity.
11. Check robustness, anomalies, and adversarial explanations.
12. Evaluate long-term ecosystem risk.
13. Choose one decision label.
14. State missing evidence and next steps.

---

## 1. Core Principle

An ads experiment should estimate durable incremental value while protecting the three-sided ecosystem:

1. users;
2. advertisers;
3. the platform.

A good ads experiment does not ask only:

> Did ads revenue, CTR, or conversions go up?

It asks:

> Did the change create incremental value that would not have happened otherwise, without degrading user trust, advertiser ROI, marketplace efficiency, or long-term revenue quality?

Ads experiments are risky because common metrics can move in misleading ways:

- CTR can rise because ads became more relevant, but also because they became intrusive, confusing, or easier to click by accident.
- Attributed conversions can rise because attribution windows changed, not because ads created new demand.
- Short-term revenue can rise because ad load increased, while long-term user satisfaction, ad blindness, or retention worsens.
- Advertiser spend can rise because the auction extracts more budget, while advertiser ROI declines.
- A targeting model can appear better by finding users who would have converted anyway.
- A marketplace ads product can shift demand between sellers rather than create new demand.
- A ranking model can increase platform revenue while crowding out organic quality or long-term advertiser value.

The agent should treat ads experiments as causal-economic systems, not simple metric comparisons.

---

## 2. Why Ads Experiments Are Different

Ads experiments differ from ordinary product A/B tests because ads systems combine causal measurement, auctions, budgets, user attention, advertiser incentives, and platform revenue.

Important differences:

1. **Attribution is not incrementality.** A conversion attributed to an ad is not necessarily caused by the ad.
2. **Exposure is endogenous.** Delivery systems optimize who sees ads. High-propensity users may receive more ads, making observational comparisons biased.
3. **Budgets and auctions create interference.** Treating one advertiser, user group, or ad slot can change prices, competition, pacing, and exposure elsewhere.
4. **Revenue can be borrowed from the future.** More ad load can improve short-term revenue while reducing future clicks, usage, trust, or advertiser demand.
5. **CTR is often diagnostic, not strategic.** CTR can be useful, but a CTR lift alone does not prove advertiser value or user value.
6. **Conversions vary in quality.** A refunded order, accidental click, duplicate lead, or low-retention signup should not be valued like a durable high-margin customer.
7. **Multiple stakeholders matter.** Ads experiments must balance user experience, advertiser return, and platform economics.

---

## 3. Historical Progression of Ads Experimentation

The agent should understand how ads measurement evolved.

### 3.1 Naive performance reporting

Early ads analysis often relied on impressions, clicks, CTR, last-click conversions, attributed revenue, and platform-reported ROAS. These metrics are useful for operations but weak for causal decision-making. They answer what happened after ads were shown, not what would have happened without the ads.

### 3.2 Attribution models

Teams then used attribution windows and multi-touch attribution to assign credit across channels or touchpoints:

- last-click attribution;
- first-click attribution;
- linear attribution;
- time-decay attribution;
- position-based attribution;
- algorithmic attribution.

These methods can help reporting and budget heuristics, but they are not automatically causal. They can over-credit ads if the user was already likely to convert.

### 3.3 Randomized holdouts and conversion lift

To estimate causality, platforms and advertisers use randomized holdout tests:

- treatment group is eligible to see the campaign;
- control group is withheld from campaign exposure;
- the difference in conversion outcomes estimates incremental lift.

This moves analysis from attribution toward incrementality.

### 3.4 PSA experiments

Public Service Announcement tests compare a real ad against a placebo-style ad. They are useful when the platform wants to control for the effect of receiving any ad impression.

PSA tests can answer:

> Did this specific advertiser message create incremental value beyond seeing a neutral ad?

Limitations:

- PSA impressions can be expensive;
- PSA creatives may not be neutral;
- PSA delivery may not match the real auction baseline;
- PSA tests can distort user experience or inventory economics.

### 3.5 Ghost Ads and predicted Ghost Ads

Ghost Ads compare exposed treatment users to control users who would have seen the same ad opportunity, without actually serving a placebo ad to the control group. This is especially useful in optimized ad systems because the control group must represent users who would have been exposed under the treatment policy, not all users in a random holdout.

Ghost Ads help the agent reason about:

- counterfactual exposure;
- treatment-on-the-treated effects;
- ad delivery optimization;
- cost-efficient incrementality testing;
- dilution in intent-to-treat designs.

### 3.6 Geo experiments and switchbacks

When user-level randomization is not clean, teams often use geography or time-based designs:

- geo holdout;
- matched market test;
- synthetic control;
- switchback test;
- interrupted time series.

These are common for large campaigns, cross-channel marketing, marketplace interventions, and ads systems where individual-level treatment is contaminated by interference.

### 3.7 Marketplace and auction-aware experimentation

Modern ads experimentation accounts for:

- advertiser budget constraints;
- bid landscapes;
- auction prices;
- ad load;
- organic displacement;
- sponsored listing substitution;
- creator or seller incentives;
- long-term advertiser retention;
- user fatigue and ad blindness.

Mature ads experimentation is a combination of experimentation, causal inference, auction economics, and product strategy.

---

## 4. Decision Labels

The agent should use exactly one primary decision label.

Allowed labels:

- `ship_ads_change`
- `ship_with_monitoring`
- `limited_rollout`
- `optimize_for_segment`
- `investigate_further`
- `do_not_trust_result`
- `do_not_ship`
- `run_incrementality_test`
- `use_geo_or_switchback`
- `use_cluster_or_marketplace_design`
- `use_quasi_experiment`

The agent may recommend a secondary action, but the final answer should contain one primary label.

---

## 5. Label Boundary Rules

Use `ship_ads_change` only when:

- the experiment is trustworthy;
- the causal estimand matches the decision;
- the incrementality or revenue-quality effect is practically meaningful;
- user and advertiser guardrails are stable;
- no important segment is materially harmed;
- auction or interference risk is low or accounted for;
- long-term risk is low or explicitly monitored.

Use `ship_with_monitoring` when evidence is positive, risks are manageable, guardrails are within tolerance, the decision is reversible, and explicit post-launch monitoring plus rollback thresholds are defined.

Use `limited_rollout` when the result is promising but full rollout is not justified because long-term, segment, or auction risk remains.

Use `optimize_for_segment` when the treatment is beneficial for one segment but neutral or harmful elsewhere, and targeting can isolate the beneficial population.

Use `investigate_further` when evidence is directionally interesting but underpowered, ambiguous, incomplete, or mechanistically unclear.

Use `do_not_trust_result` when SRM, assignment, exposure, logging, filtering, attribution, or pipeline validity fails.

Use `do_not_ship` when expected harm outweighs benefit, or when user experience, advertiser value, conversion quality, or long-term health deteriorates beyond tolerance.

Use `run_incrementality_test` when the user provides attributed metrics only and the business question is causal.

Use `use_geo_or_switchback` when user-level randomization is contaminated or the treatment changes system-wide supply, demand, auction pressure, or ad load.

Use `use_cluster_or_marketplace_design` when interference is likely across advertisers, sellers, creators, listings, geographies, or auctions.

Use `use_quasi_experiment` when randomized testing is unavailable or inappropriate, and causal impact must be estimated from observational rollout data with explicit assumptions.

---

## 6. Ads Risk Tiers

### 6.1 `low_risk_reporting_or_creative`

Examples:

- creative copy test;
- landing-page message test;
- low-budget campaign experiment;
- non-ranking reporting UI change;
- internal dashboard metric definition change.

Evidence standard:

- valid assignment or clean comparison;
- practical metric movement;
- basic quality and fraud checks;
- stable attribution definitions.

### 6.2 `medium_risk_campaign_optimization`

Examples:

- targeting expansion;
- budget allocation update;
- bid strategy change for a subset of advertisers;
- campaign objective optimization;
- frequency-cap adjustment;
- retargeting logic.

Evidence standard:

- incrementality or strong causal design;
- advertiser value metrics;
- user feedback guardrails;
- segment analysis;
- spend and conversion-quality checks.

### 6.3 `high_risk_ads_marketplace`

Examples:

- ad ranking model change;
- auction mechanism change;
- pricing reserve change;
- broad ad load change;
- relevance model change;
- marketplace sponsored listing ranking;
- ads quality model update;
- new ad placement.

Evidence standard:

- causal experiment aligned with the marketplace estimand;
- auction and interference analysis;
- user experience guardrails;
- advertiser ROI and retention guardrails;
- long-term holdout or post-launch monitoring;
- rollback thresholds.

### 6.4 `critical_risk_policy_privacy_or_trust`

Examples:

- targeting policy change;
- sensitive category ads;
- privacy-sensitive attribution change;
- underage user ad experience;
- political, financial, medical, housing, or employment ads;
- enforcement policy for advertisers;
- advertiser eligibility or account penalty logic.

Evidence standard:

- conservative causal design;
- legal, policy, and compliance review where relevant;
- fairness and protected-segment analysis;
- strict guardrails;
- auditable logs;
- long-term monitoring.

---

## 7. Metric Hierarchy for Ads Experiments

The agent must classify metrics before making a decision.

### 7.1 Decision Metric / OEC

The ads OEC should represent durable value, not shallow activity.

Possible ads OECs:

- incremental profit;
- incremental gross margin;
- incremental advertiser value;
- long-term revenue per user adjusted for user satisfaction;
- quality-adjusted ad revenue;
- advertiser lifetime value;
- user-satisfaction-adjusted RPM;
- marketplace total value;
- incremental high-quality conversions;
- long-term platform value.

The OEC should answer:

> Does this change create durable economic value after accounting for user experience and advertiser value?

### 7.2 Success Metrics

Examples:

- incremental conversions;
- incremental revenue;
- incremental profit;
- iROAS;
- conversion lift;
- qualified conversion rate;
- advertiser ROI;
- advertiser spend retention;
- fill rate;
- auction revenue per opportunity;
- value per impression;
- ad relevance score;
- landing-page quality;
- high-quality click rate;
- campaign objective completion.

### 7.3 Guardrail Metrics

User guardrails:

- user retention;
- session abandonment;
- ad hide/report rate;
- negative feedback per user;
- complaint rate;
- unsubscribe or opt-out rate;
- ad fatigue indicators;
- bounce after ad click;
- page latency;
- app crash rate;
- content satisfaction;
- search/task success rate.

Advertiser guardrails:

- advertiser ROI;
- CPA;
- conversion quality;
- refund or cancellation rate;
- repeat purchase rate;
- advertiser retention;
- advertiser churn;
- budget exhaustion quality;
- delivery stability;
- pacing stability;
- cost per qualified action.

Marketplace guardrails:

- auction competitiveness;
- bid landscape health;
- price inflation;
- organic displacement;
- seller/creator fairness;
- ad diversity;
- concentration of impressions;
- inventory liquidity;
- small advertiser access;
- winner-take-all dynamics.

Platform guardrails:

- long-term revenue;
- support tickets;
- trust/safety violations;
- policy violation rate;
- fraud rate;
- bot click rate;
- latency;
- infrastructure cost.

### 7.4 Diagnostic Metrics

Diagnostic metrics explain mechanism but should not usually drive the decision alone:

- CTR;
- impressions;
- clicks;
- CPC;
- CPM;
- CPA;
- viewability;
- frequency;
- reach;
- time to first ad;
- scroll depth;
- auction win rate;
- predicted CTR;
- predicted conversion rate;
- bid density;
- ad load;
- ads per session;
- attributed conversions;
- attribution-window conversions.

A diagnostic lift is not enough for launch if incrementality, advertiser value, or user guardrails do not support it.

### 7.5 Value Quality Metrics

Ads experiments must distinguish conversion quantity from conversion quality.

Examples:

- incremental high-margin orders;
- net revenue after refunds;
- cancellation-adjusted conversions;
- repeat-purchase conversion value;
- customer lifetime value;
- fraud-adjusted conversion value;
- advertiser-defined qualified leads;
- downstream activation after conversion;
- chargeback rate;
- trial-to-paid conversion;
- subscription retention after acquisition.

The agent should not treat every conversion as equal.

---

## 8. Required Pre-Analysis Contract

Before reading results, the experiment should specify:

- causal question;
- estimand;
- decision owner;
- risk tier;
- treatment and control;
- randomization unit;
- exposure definition;
- primary ads OEC;
- success metrics;
- user guardrails;
- advertiser guardrails;
- marketplace guardrails;
- statistical method;
- power target;
- minimum detectable effect;
- minimum practical effect;
- maximum acceptable harm thresholds;
- segment plan;
- fraud and bot filters;
- attribution window;
- conversion deduplication rule;
- excluded events;
- planned duration;
- peeking policy;
- rollout decision rule;
- rollback criteria.

The agent should penalize results that change the decision rule after seeing data.

### 8.1 Budget Siphoning & Pacing Integrity

Ads agents must detect if a Treatment "steals" volume not because it's better, but because it exhausts shared budgets/pacing faster.
- **Check:** Did Treatment spend significantly more or faster than Control? 
- **Risk:** If budgets are shared or constrained at the advertiser level, a "lift" in Treatment might be purely due to budget siphoning from Control, leading to a zero-sum gain at the platform level.
- **Agent Action:** If spend delta > 5% without an explicit budget increase in the experiment design, flag as `potential_budget_interference`.

---

## 9. Causal Estimands

The agent should identify the estimand before judging the experiment.

### 9.1 Attributed effect

What the platform credits to ads under an attribution rule. Use for reporting and diagnostics, not causal launch decisions.

### 9.2 Intent-to-treat effect

Effect of assignment to ad eligibility or campaign treatment. Useful when not everyone assigned to treatment is exposed. It can be diluted when many treatment users never see the ad.

### 9.3 Treatment-on-the-treated effect

Effect among users who actually received the ad opportunity. Useful when Ghost Ads identify control users who would have been exposed.

### 9.4 Incremental conversion effect

Conversions caused by the ads beyond natural baseline conversions. This is the main estimand for advertiser effectiveness.

### 9.5 Incremental profit effect

Incremental profit after ad cost, discounts, refunds, fulfillment cost, and margin. This is often better than incremental revenue.

### 9.6 Auction total effect

Total marketplace impact of an ads system change, including price, allocation, and spillover effects. Needed for ranking, auction, ad load, sponsored marketplace, and budget/pacing interventions.

### 9.7 Long-term user-learning effect

Change in future user behavior caused by repeated ad exposure. Needed for ad load, ad quality, ad placement, intrusive formats, and frequency cap changes.

### 9.8 Advertiser lifetime effect

Change in future advertiser behavior caused by treatment. Needed for ROI tradeoffs, advertiser retention, budget growth, auction trust, and small advertiser health.

---

## 10. Experiment Design Selection

The agent should choose design based on the causal question.

### 10.1 Standard user-level randomized experiment

Use when users can be independently randomized, interference is low, exposure logging is reliable, and the treatment does not materially change auction competition.

Good for:

- ad format UI changes;
- minor placement changes;
- creative rendering changes;
- user-facing ad experience tests with limited spillover.

Do not use alone when auction prices are affected globally, advertisers share budgets across users, inventory is scarce, ad load changes platform-wide, or treatment users influence control users.

### 10.2 Campaign holdout / conversion lift

Use when estimating whether a campaign caused incremental conversions. Treatment users are eligible for ads; control users are withheld from campaign exposure.

Key checks:

- randomization before exposure;
- no leakage into control through other campaigns;
- identical measurement windows;
- conversion deduplication;
- natural conversion rate in control;
- power for low base-rate outcomes.

### 10.3 PSA experiment

Use when a placebo ad is needed to control for receiving any ad impression.

Good for:

- brand/message testing;
- isolating specific creative content;
- testing whether real ads outperform neutral ad exposure.

Risks:

- PSA cost;
- PSA not neutral;
- different auction behavior;
- user experience distortion.

### 10.4 Ghost Ads

Use when estimating causal effect of ad exposure in optimized delivery systems and control users should represent those who would have seen the ad.

Required logs:

- auction opportunity;
- winning ad candidate;
- predicted treatment eligibility;
- counterfactual exposure flag;
- user assignment;
- impression/click/conversion outcome;
- auction context;
- bid and budget state.

Failure modes:

- counterfactual logging bug;
- predicted exposure not matching actual auction behavior;
- treatment affects future auction eligibility;
- budget feedback loops;
- missing control opportunities.

### 10.5 Geo experiment

Use when user-level randomization is contaminated, cross-channel campaigns are involved, spend cannot be withheld at user level, or media mix/offline conversions are measured.

Key requirements:

- matched geographies;
- pre-period balance;
- seasonality adjustment;
- spillover checks;
- sufficient number of regions;
- no major concurrent local shocks.

### 10.6 Switchback experiment

Use when treatment affects the entire marketplace or auction environment and can alternate over time.

Good for:

- ad load policies;
- auction ranking changes;
- marketplace supply/demand interventions;
- pricing or reserve changes;
- delivery algorithm changes.

Key requirements:

- time blocks long enough for stabilization;
- washout periods if carryover exists;
- balanced calendar effects;
- no predictable manipulation by participants;
- robust standard errors by time block.

### 10.7 Cluster randomization

Use when units interact strongly and spillovers occur within clusters more than across clusters.

Good for:

- marketplace ads;
- sponsored listings;
- local services ads;
- creator monetization;
- social or feed ads;
- inventory allocation experiments.

Cluster candidates:

- geography;
- advertiser category;
- marketplace subgraph;
- query category;
- seller/listing clusters;
- user-market clusters.

### 10.8 Advertiser-level randomization

Use when treatment is applied to advertiser tools, bidding algorithms, reporting, or budget recommendations.

Risks:

- advertiser learning;
- budget reallocation across campaigns;
- selection into adoption;
- account manager influence;
- heterogeneous advertiser sophistication.

### 10.9 Quasi-experimental design

Use when randomized evidence is unavailable.

Possible methods:

- difference-in-differences;
- synthetic control;
- regression discontinuity;
- instrumental variables;
- matching or weighting;
- interrupted time series;
- causal impact models;
- geo-based synthetic control.

Required caution:

- state identifying assumptions;
- test pre-trends;
- run placebo tests;
- assess covariate balance;
- report sensitivity to model choices;
- avoid causal overclaiming.

---

## 11. Attribution and Value Modeling

Ads experiments must separate attribution from causality.

### 11.1 Attribution window discipline

Inspect:

- click-through window;
- view-through window;
- conversion timestamp;
- attribution timestamp;
- deduplication rule;
- cross-device identity;
- conversion lag;
- refund or cancellation lag;
- delayed offline upload;
- attribution changes during the experiment.

If attribution definitions changed during the test, use `do_not_trust_result` or `investigate_further`.

### 11.2 Natural conversion baseline

The control group estimates conversions that happen without the tested ads.

Request or compute:

- treatment conversion rate;
- control conversion rate;
- absolute lift;
- relative lift;
- incremental conversions;
- incremental revenue;
- incremental profit;
- iROAS;
- cost per incremental conversion;
- confidence interval for incremental value.

### 11.3 iROAS logic

ROAS from attributed conversions can be misleading.

```text
iROAS = incremental revenue / incremental ad spend
incremental profit ROAS = incremental contribution margin / incremental ad spend
```

A campaign can have high attributed ROAS and low or negative iROAS if it targets users who would have converted anyway.

### 11.4 Conversion quality adjustment

Discount conversions that are:

- refunded;
- canceled;
- fraudulent;
- low margin;
- low retention;
- unqualified leads;
- accidental signups;
- duplicate conversions;
- driven by discounts without durable value.

### 11.5 Budget incrementality

When budget increases, ask:

- Did total conversions rise, or did attribution shift across channels?
- Did marginal CPA worsen?
- Did the campaign saturate high-intent users?
- Did increased spend cannibalize organic or existing paid channels?
- Did auction prices rise due to self-competition?
- Did the advertiser gain durable customers or pull demand forward?

---

## 12. Auction Dynamics Framework

Ads experiments should account for auctions when treatment changes ranking, bidding, pricing, supply, or demand.

### 12.1 Auction metrics to inspect

- ad opportunities;
- eligible ads per opportunity;
- bid density;
- auction win rate;
- reserve price pass rate;
- average CPC/CPM/CPA;
- clearing price;
- price per quality-adjusted impression;
- advertiser spend distribution;
- impression share;
- budget exhaustion;
- pacing stability;
- small advertiser participation;
- concentration of winners;
- organic displacement;
- ad diversity;
- quality score distribution.

### 12.2 Crowding out

Crowding out occurs when treatment increases one advertiser's or surface's performance by reducing another's.

Examples:

- sponsored listings steal conversions from organic listings;
- one advertiser's ads take conversions from another advertiser in the same platform;
- retargeting captures users who would have returned organically;
- higher ad load shifts clicks from organic results to ads;
- a ranking model favors high-bid advertisers and reduces small advertiser access.

The agent should not count shifted value as full incremental ecosystem value.

### 12.3 Auction price effects

A treatment may increase platform revenue by raising auction prices rather than creating more advertiser value.

Check:

- did advertiser ROI decline?
- did CPC increase without conversion quality improvement?
- did small advertisers lose impression share?
- did high-value advertisers reduce future spend?
- did the model extract surplus in a way that harms long-term advertiser trust?

### 12.4 Budget feedback loops

Automated delivery systems react to performance.

Check whether treatment changed:

- pacing;
- budget exhaustion timing;
- budget allocation across audiences;
- learning-phase behavior;
- optimizer exploration;
- cross-campaign cannibalization.

If feedback is substantial, simple user-level A/B readouts may not estimate the total effect.

### 12.5 Budget Siphoning & Pacing Integrity

Ads agents must detect if a Treatment "steals" volume not because it's better, but because it exhausts shared budgets/pacing faster.
- **Check:** Did Treatment spend significantly more or faster than Control? 
- **Risk:** If budgets are shared or constrained at the advertiser level, a "lift" in Treatment might be purely due to budget siphoning from Control, leading to a zero-sum gain at the platform level.
- **Agent Action:** If spend delta > 5% without an explicit budget increase in the experiment design, flag as `potential_budget_interference`.

---

## 13. Multi-Objective Tradeoff Framework

Ads decisions are rarely single-objective. The agent should explicitly balance:

1. platform revenue;
2. advertiser value;
3. user experience.

A strong ads decision avoids optimizing one stakeholder by extracting value from another.

### 13.1 Platform revenue

Revenue metrics:

- RPM;
- ARPU;
- ad revenue per session;
- take rate;
- auction revenue;
- gross ad spend;
- contribution margin;
- long-term revenue.

Revenue is not sufficient if it damages users or advertisers.

### 13.2 Advertiser value

Advertiser metrics:

- iROAS;
- CPA;
- qualified conversions;
- conversion quality;
- budget retention;
- renewal rate;
- incremental customer value;
- spend growth among healthy advertisers;
- advertiser satisfaction or support tickets.

A platform should not optimize short-term revenue if advertisers receive worse value and reduce future spend.

### 13.3 User experience

User metrics:

- retention;
- abandonment;
- ad fatigue;
- ad hides/reports;
- page latency;
- task success;
- opt-outs;
- negative feedback;
- long-term propensity to engage with ads;
- satisfaction survey metrics.

A platform should not optimize ad revenue by degrading the user's core product experience.

### 13.4 Non-inferiority logic for guardrails

Guardrails do not always need to improve. They often need to avoid unacceptable harm.

Example thresholds:

- ad hide/report rate must not increase by more than 0.05 percentage points;
- p95 ad load latency must not increase by more than 50 ms;
- high-value user 28-day retention must not decline by more than 0.1 percentage points;
- advertiser iROAS must not decline by more than 2%;
- small advertiser impression share must not decline by more than 3%;
- cancellation-adjusted conversion quality must not decline by more than 1%;
- support tickets per advertiser must not increase by more than 5%.

If a guardrail exceeds tolerance, prefer `do_not_ship` or `investigate_further`.

### 13.5 The Advertiser ROI Veto

A Top-tier Agent must protect the "demand side" of the marketplace.
- **Logic:** If Platform Revenue ↑ but Advertiser CPA (Cost Per Acquisition) ↑ or ROAS (Return on Ad Spend) ↓ significantly, this is a **Soft Breach**.
- **Reasoning:** Short-term revenue gain at the expense of advertiser profitability leads to churn.
- **Threshold:** If Advertiser ROAS drops > 3% with statistical significance, the Agent should recommend `do_not_ship` or `investigate_further` even if Revenue/CTR are positive.

---

## 14. Validity First

Before interpreting lift, validate the experiment.

### 14.1 Assignment checks

Check:

- correct randomization unit;
- stable assignment;
- expected traffic split;
- no self-selection into variants;
- no user/account duplication imbalance;
- no carryover from prior experiments;
- no eligibility drift.

### 14.2 SRM checks

Run SRM before analyzing results.

SRM can occur due to:

- bucketing bugs;
- exposure-triggered analysis bias;
- logging loss;
- bot filtering;
- variant-specific load failures;
- redirect errors;
- post-treatment exclusions;
- data joins that drop one variant more often.

If SRM is serious and undiagnosed, use `do_not_trust_result`.

### 14.3 Exposure checks

Ads experiments require exposure discipline.

Check:

- assigned population;
- eligible population;
- exposed population;
- impression logs;
- click logs;
- conversion logs;
- ghost exposure logs if used;
- ad opportunity logs;
- auction context logs;
- control leakage;
- treatment noncompliance.

The agent should distinguish assignment, eligibility, and exposure.

### 14.4 Logging and telemetry checks

Check:

- impression logging completeness;
- click logging completeness;
- conversion logging completeness;
- deduplication;
- timestamp alignment;
- timezone consistency;
- server/client logging differences;
- ad blocker effects;
- privacy consent effects;
- offline conversion upload delays;
- attribution pipeline changes.

### 14.5 Filtering bias

Filtering can create biased results if treatment changes the probability of being included.

Check:

- bot filters;
- fraud filters;
- viewability filters;
- eligibility filters;
- advertiser policy filters;
- conversion quality filters;
- triggered analysis criteria;
- missing-user filters;
- outlier trimming.

A treatment that changes engagement can also change whether users pass filters.

### 14.6 Latency and load checks

Ad loading can affect both exposure and outcomes.

Check:

- ad request latency;
- auction latency;
- page load latency;
- render latency;
- p95 and p99 latency;
- timeout rate;
- blank ad rate;
- layout shift;
- treatment-specific failure rate.

If treatment reduces latency, it may increase logged impressions and conversions for reasons partly unrelated to ad quality. If treatment increases latency, it may suppress downstream user behavior.

### 14.7 Post-click Selection Bias (Conditioning on Clicks)

When analyzing CVR (Conversion Rate), the Agent must check if the Treatment changed the *composition* of users who click. 
- **Example:** If Treatment attracts more "accidental" or "low-intent" clickers, CTR will go up, but CVR will drop. This isn't a failure of the landing page, but a failure of the ad targeting quality.
- **Agent Action:** Always compare "Conversions per Impression" (Total Value) alongside "Conversions per Click" (Efficiency) to disentangle targeting changes from intent changes.

---

## 15. Segment Scan

Averages can hide harm.

User segments:

- new vs existing users;
- high-value vs low-value users;
- heavy vs light users;
- paid vs free users;
- logged-in vs logged-out users;
- acquisition channel;
- geography;
- platform;
- device;
- network quality;
- privacy consent status;
- policy-sensitive groups where legally and ethically allowed;
- ad blocker users where measurable.

Advertiser segments:

- small vs large advertisers;
- new vs mature advertisers;
- high-spend vs low-spend advertisers;
- high-quality vs low-quality advertisers;
- vertical/category;
- campaign objective;
- bidding strategy;
- budget size;
- margin profile;
- brand vs performance advertisers;
- agency-managed vs self-serve advertisers.

Marketplace segments:

- high-demand vs low-demand geographies;
- supply-constrained vs demand-constrained markets;
- query category;
- organic result quality;
- inventory scarcity;
- seller/creator category;
- sponsored vs organic competition intensity.

Interpret segment effects with caution:

- distinguish pre-specified segments from exploratory scans;
- adjust for multiple testing or label exploratory findings;
- avoid overreacting to tiny noisy slices;
- prioritize strategically important or vulnerable segments;
- require action when harm is large, credible, and business-relevant.

---

## 16. Long-Term and Ecosystem Risk

Short-term ads experiments can miss delayed harm.

### 16.1 User learning

Repeated ad exposure can change users' future behavior.

Risks:

- ad blindness;
- ad fatigue;
- lower click propensity;
- lower platform usage;
- lower trust;
- more ad blocking;
- lower satisfaction;
- more complaints.

Use:

- long-term holdout;
- cohort rollout;
- repeated exposure analysis;
- frequency response curves;
- delayed retention metrics;
- long-term CTR or ad sightedness proxies.

### 16.2 Advertiser learning

Advertisers respond to performance.

Risks:

- future spend reduction;
- budget migration to competitors;
- lower trust in reporting;
- higher support load;
- strategic bidding changes;
- campaign churn;
- small advertiser exit.

Use:

- advertiser retention cohorts;
- repeat budget behavior;
- post-treatment spend trajectory;
- account-level satisfaction;
- longer measurement windows.

### 16.3 Marketplace health

Ads can distort the marketplace.

Risks:

- organic quality degradation;
- excessive winner concentration;
- reduced small advertiser access;
- reduced seller liquidity;
- lower content diversity;
- lower user trust in results;
- low-quality advertisers outbidding high-quality experiences.

Use:

- diversity metrics;
- concentration metrics;
- supply/demand balance;
- seller/creator retention;
- query/category-level monitoring;
- marketplace-level holdouts.

### 16.4 Long-term holdout policy

Use long-term holdouts when:

- treatment changes ad load;
- treatment changes ranking or auction quality;
- treatment affects advertiser incentives;
- short-term and long-term revenue may diverge;
- user fatigue is plausible;
- treatment is hard to reverse psychologically or economically.

---

## 17. Interference and Network Effects

Standard A/B testing assumes one unit's treatment does not affect another unit's outcome. Ads systems often violate this assumption.

Sources of interference:

- auctions;
- shared advertiser budgets;
- shared inventory;
- organic result displacement;
- seller competition;
- user attention competition;
- cross-device identity;
- social sharing;
- remarketing pools;
- frequency caps;
- campaign learning systems;
- pacing algorithms.

Symptoms of interference:

- treatment changes control group prices;
- control group conversion rate moves unexpectedly;
- auction win rates shift in both variants;
- advertisers reallocate budgets;
- organic traffic declines when ads rise;
- seller outcomes move in opposite directions;
- treatment effects vary by market tightness;
- effects disappear when measured at marketplace level.

Design guidance:

- use individual randomization when interference is low;
- use cluster randomization when spillovers are local within groups;
- use switchback when treatment affects the whole market at a time;
- use geo experiments when cross-channel or system-wide campaigns cannot be randomized individually;
- use quasi-experiments only when randomized designs are not feasible, and state assumptions clearly.

---

## 18. Robustness and Adversarial Diagnostics

The agent should behave like a skeptical investigator.

### 18.1 Suspicious CTR increase

If CTR rises sharply, check:

- accidental clicks;
- misleading creative;
- layout shift;
- ad placement moved closer to primary action;
- click logging duplication;
- bot traffic;
- incentivized clicks;
- lower-quality placements;
- lower post-click engagement;
- higher bounce rate;
- lower conversion rate after click;
- higher complaints or hides;
- mobile fat-finger rate.

CTR lift is not a win if click quality deteriorates.

### 18.2 Suspicious conversion increase

If conversions rise sharply, check:

- attribution window change;
- conversion deduplication bug;
- delayed conversion upload;
- retargeting high-intent users;
- organic cannibalization;
- duplicate orders;
- refunds or cancellations;
- large outlier orders;
- internal/test traffic;
- bot or fraud conversions;
- coupon leakage;
- seasonality or external event.

### 18.3 Suspicious revenue increase

If revenue rises, check:

- advertiser ROI;
- user retention;
- ad load;
- CPC inflation;
- auction price changes;
- concentration among few advertisers;
- budget exhaustion;
- small advertiser harm;
- organic cannibalization;
- refund-adjusted value;
- long-term revenue proxy.

### 18.4 Suspicious null result

If no effect is detected, check:

- underpowering;
- dilution from unexposed assigned users;
- control contamination;
- weak treatment intensity;
- wrong attribution window;
- conversion lag;
- poor segment targeting;
- treatment not delivered;
- high variance from outliers.

Null does not always mean no effect.

### 18.5 Outlier and fraud robustness

Always inspect:

- winsorized and raw estimates;
- top spender exclusion;
- top order exclusion;
- bot-filtered vs unfiltered estimates;
- user-level vs event-level aggregation;
- advertiser-level cluster-robust uncertainty;
- pre-period balance for high-value users;
- conversion quality by order size;
- refund-adjusted estimates.

---

## 19. Practical Significance

Statistical significance is not enough.

Ask:

- Is the lift large enough to matter after costs?
- Does the effect exceed the minimum practical effect?
- Does the lower bound of the confidence interval still justify action?
- Is the lift meaningful relative to historical variance?
- Does the lift survive quality adjustment?
- Does the lift scale beyond the tested segment?
- Does it justify engineering, sales, policy, and operational cost?
- Does it improve durable value rather than a shallow proxy?

Examples:

- A 5% attributed conversion lift may not matter if incremental lift is near zero.
- A 2% revenue lift may be unattractive if advertiser ROI drops 4%.
- A 0.5% revenue lift may be valuable if user and advertiser guardrails are stable and scale is large.
- A statistically insignificant user retention decline may still block launch if downside risk is high and the test is underpowered.

---

## 20. Scenario Playbooks

### 20.1 Campaign incrementality

Question:

> Did this campaign cause incremental conversions?

Required design:

- randomized holdout;
- Ghost Ads;
- PSA;
- geo experiment;
- or clean quasi-experiment.

Primary metrics:

- incremental conversions;
- incremental revenue;
- incremental profit;
- iROAS;
- cost per incremental conversion.

Guardrails:

- conversion quality;
- refunds;
- user complaints;
- frequency;
- overlap with other channels;
- brand safety;
- long-term customer value.

Decision logic:

- If attributed ROAS is high but iROAS is weak, do not scale without further testing.
- If iROAS is strong and conversion quality is stable, scale with monitoring.
- If control contamination exists, use `do_not_trust_result` or rerun.

### 20.2 Ad load increase

Question:

> Should we show more ads?

Primary metrics:

- long-term revenue per user;
- user-satisfaction-adjusted RPM;
- incremental revenue after user-learning adjustment.

Guardrails:

- retention;
- ad hides/reports;
- session abandonment;
- task success;
- ad fatigue;
- latency;
- long-term CTR;
- user complaints.

Decision logic:

- Do not ship based only on short-term RPM.
- Require long-term holdout or strong user-learning proxy.
- If revenue rises but high-value user retention falls beyond tolerance, do not ship.
- If short-term revenue is positive and user guardrails are stable, consider limited rollout with long-term holdout.

### 20.3 Ad ranking model change

Question:

> Should we launch a new ad ranking or relevance model?

Primary metrics:

- quality-adjusted revenue;
- advertiser value;
- user-satisfaction-adjusted RPM;
- long-term platform value.

Guardrails:

- advertiser ROI;
- conversion quality;
- ad hides/reports;
- latency;
- small advertiser access;
- auction concentration;
- policy violation rate.

Decision logic:

- Do not ship if revenue rises by overpricing low-quality ads.
- Analyze bidder and category segments.
- Use cluster, switchback, or careful ramp if auction interference is likely.
- Require rollback thresholds for advertiser ROI and user negative feedback.

### 20.4 Auction mechanism change

Question:

> Should we change auction pricing, reserve prices, quality scores, or ranking objective?

Primary metrics:

- marketplace total value;
- long-term platform revenue;
- advertiser surplus proxy;
- user-quality-adjusted revenue.

Guardrails:

- advertiser ROI;
- churn;
- bid density;
- small advertiser participation;
- CPC inflation;
- winner concentration;
- user satisfaction.

Decision logic:

- Treat as high-risk ads marketplace.
- Individual-level A/B may be biased if auctions interact.
- Prefer switchback, cluster, or marketplace-level design.
- Do not ship if revenue is extracted through unsustainable advertiser ROI deterioration.

### 20.5 Targeting expansion

Question:

> Should we broaden the audience?

Primary metrics:

- incremental conversions;
- marginal CPA;
- marginal iROAS;
- conversion quality.

Guardrails:

- frequency;
- user complaints;
- opt-outs;
- brand safety;
- advertiser ROI;
- audience saturation.

Decision logic:

- Compare marginal users, not just total campaign performance.
- Watch for lower intent and conversion quality.
- If attributed conversions rise but iROAS falls, investigate or restrict.

### 20.6 Retargeting

Question:

> Does retargeting create incremental value?

Primary metrics:

- incremental conversions among retargeted audience;
- iROAS;
- incremental profit.

Guardrails:

- natural conversion baseline;
- frequency;
- user annoyance;
- view-through inflation;
- organic cannibalization;
- privacy-sensitive segments.

Decision logic:

- Retargeting is prone to over-attribution because users already have high purchase intent.
- Prefer Ghost Ads or holdout lift.
- Do not scale based on attributed ROAS alone.

### 20.7 Creative or message test

Question:

> Which creative performs better?

Primary metrics:

- incremental qualified conversion;
- conversion quality;
- creative-specific lift;
- post-click quality.

Guardrails:

- misleading clicks;
- complaints;
- brand safety;
- bounce rate;
- refund rate.

Decision logic:

- CTR is diagnostic.
- Prefer post-click and incremental outcomes.
- If creative increases CTR but lowers conversion quality, do not promote broadly.

### 20.8 Frequency cap change

Question:

> Should we increase or decrease ad frequency?

Primary metrics:

- incremental conversion per additional impression;
- marginal revenue;
- user-satisfaction-adjusted revenue.

Guardrails:

- ad fatigue;
- hides/reports;
- opt-outs;
- conversion quality;
- diminishing returns;
- long-term retention.

Decision logic:

- Estimate marginal value by frequency bucket.
- If marginal conversions flatten and negative feedback rises, reduce or cap frequency.
- Use longer readout if fatigue is likely.

### 20.9 Sponsored marketplace listings

Question:

> Should sponsored placements or seller ads be changed?

Primary metrics:

- incremental marketplace transactions;
- quality-adjusted GMV;
- buyer retention;
- seller value;
- total marketplace liquidity.

Guardrails:

- organic seller displacement;
- buyer trust;
- seller concentration;
- small seller access;
- refund rate;
- search relevance;
- marketplace fairness.

Decision logic:

- Do not count shifted seller sales as full platform incrementality.
- Use cluster, geo, or marketplace-aware designs.
- Monitor both buyer and seller outcomes.

### 20.10 Cross-channel marketing

Question:

> Did this channel add value beyond existing channels?

Primary metrics:

- total incremental conversions;
- incremental revenue/profit;
- channel-level marginal iROAS;
- total media mix effect.

Guardrails:

- channel cannibalization;
- attribution overlap;
- brand search lift;
- organic traffic displacement;
- frequency overlap;
- customer quality.

Decision logic:

- Platform-reported ROAS may double-count conversions across channels.
- Prefer geo experiments, media-mix modeling plus calibration, or randomized holdouts where possible.
- Require deduped conversion logic.

### 20.11 Privacy or attribution change

Question:

> Should we change measurement, identity, tracking, or attribution logic?

Primary metrics:

- measurement accuracy;
- privacy compliance;
- advertiser decision quality;
- modeled conversion calibration.

Guardrails:

- user privacy;
- policy compliance;
- reporting bias;
- advertiser trust;
- data loss by segment;
- calibration error.

Decision logic:

- Treat as critical risk.
- Do not compare pre/post attribution numbers as if they are causal business effects.
- Validate against experiments or trusted ground truth.

### 20.12 Ads latency or rendering change

Question:

> Did ad loading or rendering change improve ads performance?

Primary metrics:

- user task success;
- valid rendered impressions;
- revenue per eligible opportunity;
- post-render engagement quality.

Guardrails:

- page speed;
- timeout rate;
- layout shift;
- accidental clicks;
- bounce rate;
- downstream conversion quality.

Decision logic:

- More logged impressions may reflect better rendering, not better ad relevance.
- Separate exposure instrumentation improvement from user/ad value improvement.

---

## 21. Decision Matrix

| Evidence Pattern | Recommended Decision |
|---|---|
| Valid randomized incrementality test shows meaningful lift, user and advertiser guardrails stable, low interference | `ship_ads_change` |
| Incremental revenue improves, guardrails within tolerance, but long-term user fatigue remains plausible | `ship_with_monitoring` or `limited_rollout` |
| Attributed conversions improve but no causal holdout exists | `run_incrementality_test` |
| CTR improves but post-click quality, conversion rate, or complaints worsen | `investigate_further` or `do_not_ship` |
| Short-term revenue improves but high-value user retention declines beyond tolerance | `do_not_ship` |
| Platform revenue improves but advertiser ROI falls materially | `do_not_ship` or `limited_rollout` with strict advertiser guardrails |
| Ad load revenue improves but long-term ad blindness or fatigue proxy worsens | `limited_rollout` or `do_not_ship` |
| SRM, exposure logging failure, attribution bug, or conversion deduplication issue is detected | `do_not_trust_result` |
| User-level test likely suffers auction or marketplace interference | `use_cluster_or_marketplace_design` or `use_geo_or_switchback` |
| Campaign lift varies strongly by geography or market tightness | `optimize_for_segment` or `use_geo_or_switchback` |
| Strong lift only in high-intent retargeting population and natural conversion baseline is high | `investigate_further` unless Ghost Ads or holdout confirms incrementality |
| Revenue lift is driven by a few large outlier advertisers or orders | `investigate_further` |
| New ranking model improves revenue and iROAS but increases p95 latency beyond tolerance | `limited_rollout` or `do_not_ship` |
| Auction change increases CPC but reduces small advertiser participation | `investigate_further` or `do_not_ship` |
| Observational attribution suggests lift but pre-trends or selection bias are likely | `use_quasi_experiment` or `run_incrementality_test` |
| Experiment is underpowered for rare conversions and downside risk is high | `investigate_further` |
| Segment-specific benefit is credible and harmed segments can be excluded | `optimize_for_segment` |
| Broad average is positive but strategically important segment is harmed | `limited_rollout`, `optimize_for_segment`, or `do_not_ship` |

---

## 22. Required Agent Reasoning Order

For every ads experiment question, reason in this order:

1. Clarify the concrete ads decision.
2. Identify the stakeholder objective: advertiser effectiveness, platform monetization, user experience, marketplace efficiency, measurement accuracy, or policy/trust.
3. Define the causal estimand.
4. Evaluate whether the experiment design matches the estimand.
5. Validate trustworthiness: SRM, assignment, exposure, logging, deduplication, attribution, filtering, bot/fraud, latency, contamination.
6. Define metric hierarchy: OEC, success metrics, user guardrails, advertiser guardrails, marketplace guardrails, diagnostics.
7. Evaluate incrementality and value quality.
8. Evaluate auction and marketplace effects.
9. Evaluate user, advertiser, and platform guardrails.
10. Analyze segments.
11. Run adversarial diagnostics.
12. Evaluate long-term risk.
13. Choose one decision label.
14. State missing evidence and next action.

---

## 23. Minimum Evidence Required for an Ads Experiment Memo

### 23.1 Recommendation

State exactly one label:

- `ship_ads_change`
- `ship_with_monitoring`
- `limited_rollout`
- `optimize_for_segment`
- `investigate_further`
- `do_not_trust_result`
- `do_not_ship`
- `run_incrementality_test`
- `use_geo_or_switchback`
- `use_cluster_or_marketplace_design`
- `use_quasi_experiment`

### 23.2 Product and ads context

Include:

- product surface;
- ad format;
- advertisers affected;
- users affected;
- marketplace context;
- business goal;
- risk tier;
- reversibility.

### 23.3 Experiment design

Include:

- treatment;
- control;
- randomization unit;
- exposure definition;
- assignment population;
- eligible population;
- exposed population;
- sample size;
- duration;
- attribution window;
- conversion definition;
- causal estimand;
- design choice;
- interference plan;
- pre-specified decision rule.

### 23.4 Results

Report:

- OEC movement;
- incremental lift;
- attributed lift;
- absolute and relative effects;
- uncertainty interval;
- iROAS;
- conversion quality;
- user guardrails;
- advertiser guardrails;
- marketplace guardrails;
- diagnostic metrics;
- segment effects;
- long-term proxies.

### 23.5 Validity checks

Include:

- SRM;
- assignment stability;
- exposure consistency;
- logging completeness;
- deduplication;
- attribution window consistency;
- filtering bias;
- bot/fraud checks;
- latency/rendering checks;
- contamination;
- peeking or early stopping;
- power and MDE.

### 23.6 Auction and marketplace review

Include:

- auction price effects;
- budget pacing;
- crowding out;
- organic displacement;
- advertiser concentration;
- small advertiser impact;
- market tightness;
- inventory constraints;
- interference risk.

### 23.7 Robustness

Include:

- outlier sensitivity;
- bot-filtered estimate;
- conversion-quality-adjusted estimate;
- alternative attribution windows;
- segment stability;
- pre-period balance;
- placebo checks where applicable.

### 23.8 Decision and next steps

Include:

- final label;
- rollout or test plan;
- monitoring metrics;
- rollback thresholds;
- expansion criteria;
- missing evidence;
- owner if available.

---

## 24. Response Template for the Agent

```text
Decision: [ship_ads_change / ship_with_monitoring / limited_rollout / optimize_for_segment / investigate_further / do_not_trust_result / do_not_ship / run_incrementality_test / use_geo_or_switchback / use_cluster_or_marketplace_design / use_quasi_experiment]

Decision problem:
[Restate the ads decision.]

Ads context:
- Surface:
- Ad format:
- Stakeholders:
- Risk tier:
- Reversibility:

Causal estimand:
[Attributed effect / incrementality / treatment-on-the-treated / auction total effect / long-term user-learning effect / advertiser lifetime effect / marketplace total effect]

Design assessment:
[State whether the current design matches the estimand. If not, specify the correct design.]

Metric hierarchy:
- OEC:
- Success metrics:
- User guardrails:
- Advertiser guardrails:
- Marketplace guardrails:
- Diagnostic metrics:

Evidence assessment:
1.  **Causal Validity:** Is this attributed lift or incremental lift (Ghost Ads/PSA)?
2.  **Auction Integrity:** Did we just "win" more auctions by overbidding, or by better relevance?
3.  **Advertiser Impact:** Is the advertiser's ROI stable? (Crucial for long-term retention).
4.  **User Experience:** Is there an increase in negative feedback or ad fatigue?
5.  **Budget Dynamics:** Did we siphon budget from the control or other campaigns?
6.  **Selection Bias:** Is the CVR change driven by a change in clicker quality?

Recommendation:
[Clear final recommendation.]

Missing evidence:
- [Evidence 1]
- [Evidence 2]
- [Evidence 3]

Next steps:
- [Analysis/test step]
- [Monitoring/rollout step]
- [Rollback or expansion threshold]
```

---

## 25. Examples

### 25.1 Short-term revenue up, advertiser ROI down

Question:

> A new ad ranking model increases platform revenue by 5%, but advertiser ROI drops by 3%. Should we launch?

Good reasoning:

This is not automatically a win. The model may be extracting more short-term revenue from advertisers while reducing their value. Inspect iROAS, conversion quality, CPC inflation, advertiser retention, small advertiser impression share, user negative feedback, auction concentration, and segment effects.

Likely decision:

- `investigate_further` if the ROI decline is material but not fully diagnosed.
- `do_not_ship` if advertiser ROI decline exceeds tolerance.
- `limited_rollout` only if ROI harm is within tolerance and long-term advertiser monitoring is defined.

Bad answer:

> Revenue increased 5%, so launch.

### 25.2 CTR up, conversion quality down

Question:

> A new ad format increases CTR by 12%, but conversion rate after click is flat and refund rate rises. Is this good?

Good reasoning:

CTR is diagnostic. This may indicate accidental or misleading clicks. Inspect post-click quality, bounce rate, refund-adjusted value, complaints, and placement changes.

Likely decision:

- `investigate_further` or `do_not_ship`.

### 25.3 Retargeting has high ROAS

Question:

> Our retargeting campaign has 9x ROAS. Should we scale spend?

Good reasoning:

High attributed ROAS is common in retargeting because users already have high purchase intent. Ask for incrementality evidence from randomized holdout, Ghost Ads, PSA, or geo incrementality test.

Likely decision:

- `run_incrementality_test`.

### 25.4 Ad load increase

Question:

> Increasing ad load improved short-term RPM by 4%, with no statistically significant retention decline. Should we ship?

Good reasoning:

Absence of significant retention harm is not proof of safety if the test is underpowered or too short. Inspect long-term user-learning proxies, ad hides, reports, task success, high-value user retention, and long-term holdouts.

Likely decision:

- `limited_rollout` if guardrails are within tolerance but long-term risk remains.
- `do_not_ship` if negative feedback or high-value retention exceeds threshold.
- `ship_with_monitoring` only if risk is low, reversible, and monitoring is strict.

### 25.5 Auction change with user-level A/B

Question:

> We tested a reserve price change with user-level randomization. Revenue is up 2%. Is that valid?

Good reasoning:

Reserve price changes alter auction dynamics. User-level randomization may not estimate the total marketplace effect if advertisers' budgets, bids, and auction prices respond across treatment and control.

Likely decision:

- `use_geo_or_switchback` or `use_cluster_or_marketplace_design`.

### 25.6 Conversion spike

Question:

> Treatment conversions jumped 30% on day three. Can we call this a win?

Good reasoning:

A sudden conversion spike should trigger anomaly checks: attribution upload batch, duplicate conversions, bot traffic, large orders, campaign budget changes, promo/coupon events, logging deployment, conversion window changes, and seasonality.

Likely decision:

- `investigate_further` or `do_not_trust_result`.

---

## 26. Evaluation Criteria for Agent Answers

A high-quality answer should:

- choose exactly one ads-specific decision label;
- state the ads decision problem;
- identify the causal estimand;
- determine whether the design matches the estimand;
- separate attribution from incrementality;
- check validity before interpreting lift;
- define OEC, success metrics, guardrails, and diagnostics;
- evaluate user, advertiser, platform, and marketplace tradeoffs;
- inspect auction dynamics and interference;
- analyze segment heterogeneity;
- consider long-term user and advertiser learning;
- run adversarial checks for CTR, conversion, revenue, fraud, outliers, filtering, and latency;
- state uncertainty and practical significance;
- recommend concrete next steps;
- avoid overclaiming when evidence is incomplete.

Penalize an answer if it:

- recommends launch because CTR increased;
- recommends scaling because attributed ROAS is high;
- ignores incrementality;
- ignores advertiser ROI;
- ignores user experience guardrails;
- ignores auction dynamics;
- treats user-level randomization as sufficient when interference is likely;
- ignores conversion quality;
- ignores refunds, cancellations, or fraud;
- ignores outliers;
- ignores latency and rendering effects;
- ignores SRM or logging failures;
- treats short-term revenue as long-term value;
- gives generic advice without a decision label;
- asks many questions without giving a provisional decision framing;
- recommends partial rollout without defining segment, size, duration, monitoring, and expansion criteria.

A strong answer should feel like a senior ads data scientist writing a concise experiment review, not like a generic marketing analytics explanation.

---

## 27. Common Failure Modes

1. **Attribution-as-causality error**

   Treating attributed conversions as incremental conversions. Correct by requiring holdout, Ghost Ads, PSA, geo, switchback, or quasi-experimental evidence.

2. **CTR worship**

   Treating clicks as value. Correct by inspecting post-click quality, conversion quality, user feedback, and advertiser outcomes.

3. **Short-term revenue bias**

   Optimizing RPM while ignoring user fatigue and long-term ad blindness. Correct with long-term user-learning proxies and holdouts.

4. **Advertiser extraction**

   Increasing platform revenue by reducing advertiser ROI. Correct by requiring advertiser value and retention guardrails.

5. **Auction naivety**

   Ignoring budget, pacing, prices, and crowding out. Correct by inspecting auction metrics and using marketplace-aware designs.

6. **Averages-only reasoning**

   Shipping because average lift is positive while high-value users, small advertisers, or critical geographies are harmed. Correct with segment scans.

7. **Invalid experiment trust**

   Interpreting lift despite SRM, logging errors, or attribution bugs. Correct with `do_not_trust_result`.

8. **Outlier blindness**

   Letting one advertiser, bot cluster, or large order drive the result. Correct with robust estimates and outlier sensitivity.

9. **Filtering bias**

   Applying post-treatment filters that remove impacted users or events. Correct by auditing filters and comparing assigned, eligible, exposed, and analyzed populations.

10. **Interference blindness**

   Using individual-level A/B when treatment changes a shared auction or marketplace. Correct with cluster, geo, switchback, marketplace-level, or quasi-experimental design.

---

## 28. Final Rule

The agent should optimize for durable ecosystem value, not short-term ads metrics.

When incrementality is strong, value quality is high, guardrails are stable, and interference is controlled, recommend shipping.

When attributed metrics are positive but incrementality is unknown, recommend an incrementality test.

When auction or marketplace interference is likely, use cluster, geo, switchback, or marketplace-aware designs.

When CTR or revenue rises but user experience, advertiser ROI, conversion quality, or long-term health deteriorates, do not ship broadly.

When the experiment is invalid, do not interpret the measured lift as causal evidence.

The best ads experiment answer is not the most optimistic answer. It is the one that makes causality, economics, risk, uncertainty, and the next responsible action explicit.

---

## 29. Reference Notes

This playbook is informed by public experimentation and advertising measurement literature, including:

- Microsoft Experimentation Platform work on SRM and trustworthy experimentation.
- Johnson, Lewis, and Nubbemeyer, "Ghost Ads: Improving the Economics of Measuring Online Ad Effectiveness."
- Google research on long-term ads impact, ads blindness, and user-satisfaction-aware OECs.
- Abrams and Schwarz, "Ad Auction Design and User Experience."
- Gordon et al., "A Comparison of Approaches to Advertising Measurement: Evidence from Big Field Experiments at Facebook."
- Marketplace experimentation literature on interference bias, cluster randomization, switchbacks, and marketplace total effects.
