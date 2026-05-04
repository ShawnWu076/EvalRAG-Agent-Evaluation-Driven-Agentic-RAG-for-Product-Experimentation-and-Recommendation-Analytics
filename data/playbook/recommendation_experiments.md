# Recommendation Experiments Playbook

This playbook defines how an Agent should reason about recommendation-system experiments, recommendation metrics, and recommendation launch decisions.

It is designed for an evaluation-driven Agentic RAG system. The goal is not to make the Agent report that CTR, NDCG, or watch time improved. The goal is to make the Agent behave like a senior data scientist who can decide whether a recommendation change improves durable user value without exploiting short-term attention, narrowing discovery, harming supply-side incentives, or degrading trust and ecosystem health.

A recommendation system is not only a ranking model. It is a behavioral allocation system. It decides what users see, what creators or sellers receive exposure, which items get feedback, and which future data the platform will learn from. This creates feedback loops, exposure bias, popularity bias, position bias, and long-term ecosystem effects.

The Agent should treat a recommendation experiment as successful only when the change improves durable recommendation value under trustworthy experimentation, stable guardrails, interpretable mechanisms, and acceptable long-term risk.

---

## Quick Retrieval Summary

Use this playbook when the user asks about recommendation experiments, ranking experiments, feed experiments, search ranking, homepage recommendations, "For You" feeds, playlist recommendations, item/product recommendations, creator/content distribution, recommendation model launches, offline vs online recommender evaluation, CTR/watch-time tradeoffs, diversity, novelty, exposure concentration, long-term satisfaction, or whether a recommendation change should ship.

This playbook is especially relevant when:

- CTR, watch time, clicks, saves, purchases, or engagement increase;
- offline ranking metrics improve but online product metrics are unclear;
- a recommendation model changes candidate generation, ranking, reranking, blending, filtering, or personalization;
- the change may concentrate exposure among head items, creators, sellers, or content categories;
- user engagement improves but negative feedback, churn, fatigue, or content quality worsens;
- the model may exploit clickbait, repeated exposure, position effects, autoplay, or UI changes;
- historical logs may be biased because the old recommender controlled exposure;
- ordinary A/B testing may miss long-term retention, satisfaction, ecosystem, or supply-side effects;
- the user asks whether a recommendation system is "better";
- the user wants to compare offline metrics, online metrics, and launch decisions.

Default reasoning order:

1. Identify the recommendation surface and intervention.
2. Define the durable recommendation objective.
3. Separate offline, online, decision, guardrail, and ecosystem metrics.
4. Validate experiment trustworthiness and telemetry.
5. Check exposure bias, position bias, and counterfactual validity.
6. Evaluate short-term engagement against long-term satisfaction.
7. Analyze diversity, novelty, coverage, and concentration.
8. Check supply-side, creator-side, seller-side, and marketplace effects.
9. Scan segments and cohorts.
10. Decide whether to launch, monitor, investigate, redesign, or use a different evaluation design.

---

## 1. Core Principle

Optimize durable recommendation value, not clicks.

A recommendation experiment is successful only if it improves the user's ability to discover valuable content, products, people, or actions while preserving trust, diversity, satisfaction, and supply-side incentives.

The Agent should not treat the following as sufficient evidence of success:

- CTR increased;
- impressions increased;
- watch time increased;
- session length increased;
- offline NDCG improved;
- model AUC improved;
- top-K recall improved;
- purchases increased without refund/margin/repeat checks;
- engagement increased in a short experiment.

A good recommendation decision depends on:

- whether the metric movement is trustworthy;
- whether the decision metric is aligned with durable user value;
- whether short-term engagement is healthy or exploitative;
- whether users are more satisfied, not merely more reactive;
- whether recommendations remain diverse, novel, and useful;
- whether the model avoids popularity collapse and feedback loops;
- whether important user segments are harmed;
- whether creators, sellers, advertisers, or content providers are harmed;
- whether exposure concentration remains acceptable;
- whether long-term retention and return behavior are protected;
- whether the evaluation design handles exposure bias and interference.

Bad reasoning:

> CTR increased by 4%, so the recommendation model is better.

Better reasoning:

> CTR increased, but the Agent must check whether the clicks are high-quality, whether downstream completion, satisfaction, negative feedback, retention, diversity, creator/seller exposure, latency, and long-term guardrails remain stable. A CTR lift alone is not a launch reason.

---

## 2. Recommendation Surface Classification

The Agent must classify the recommendation surface before selecting metrics.

Different surfaces have different objectives, harms, and experimental designs.

### 2.1 Feed Ranking / Home Feed

Examples:

- social feed;
- short-video feed;
- news feed;
- personalized homepage;
- "For You" feed.

Core problem:

- rank a high-volume stream of candidate content while balancing relevance, satisfaction, novelty, diversity, trust, and creator incentives.

Primary questions:

- Are users seeing content they value?
- Is the feed creating healthy retention or shallow addiction?
- Are negative feedback and fatigue controlled?
- Are creators or content categories receiving sustainable exposure?
- Does the model amplify low-quality or policy-sensitive content?

Representative metrics:

- qualified engagement;
- satisfied watch/read time;
- completion quality;
- hide/report/not-interested rate;
- next-day or 7-day return;
- long-term retention;
- content diversity;
- creator exposure concentration;
- policy-violation exposure;
- user survey satisfaction.

---

### 2.2 Video / Audio / Entertainment Recommendations

Examples:

- streaming video rows;
- music playlist recommendations;
- podcast recommendations;
- "Up Next" panels;
- continue-watching surfaces.

Core problem:

- help users choose valuable media while minimizing fatigue, repetition, and shallow consumption loops.

Primary questions:

- Did the user consume more because the recommendation was valuable?
- Did the user discover new content they liked?
- Did satisfaction improve, not just autoplay volume?
- Did return behavior improve?
- Did the algorithm narrow consumption diversity?

Representative metrics:

- starts from recommendation;
- completion rate;
- skip rate;
- save/add-to-library;
- repeat listening/watching;
- long-term return;
- survey satisfaction;
- genre or artist diversity;
- novelty;
- fatigue signals.

---

### 2.3 Ecommerce / Product Recommendations

Examples:

- product detail recommendations;
- homepage personalization;
- cart recommendations;
- cross-sell / upsell modules;
- search reranking.

Core problem:

- recommend relevant products that create incremental purchase value without increasing returns, refund cost, dissatisfaction, or low-margin substitution.

Primary questions:

- Did recommendations create incremental purchases or only shift purchases?
- Did margin, return rate, and repeat purchase remain healthy?
- Did recommendations over-concentrate demand among head products or sellers?
- Did the model reduce discovery of long-tail inventory?

Representative metrics:

- recommendation-attributed purchases;
- incremental conversion;
- add-to-cart quality;
- purchase conversion;
- gross margin;
- return/refund rate;
- repeat purchase;
- product diversity;
- seller/listing exposure;
- inventory sell-through.

---

### 2.4 Marketplace / Seller / Creator Recommendations

Examples:

- promoted listings;
- seller ranking;
- creator recommendations;
- provider recommendations;
- marketplace search results.

Core problem:

- allocate demand and attention across supply while preserving buyer match quality and supply-side health.

Primary questions:

- Did buyer outcomes improve?
- Did seller or creator earnings and retention remain stable?
- Did exposure become destructively concentrated?
- Did the model crowd out untreated supply?

Representative metrics:

- buyer conversion;
- match quality;
- seller/creator exposure;
- seller/creator earnings;
- long-tail success;
- exposure concentration;
- supply retention;
- marketplace liquidity.

For marketplace-heavy cases, also use `marketplace_metrics.md`.

---

### 2.5 Search Ranking and Query Recommendations

Examples:

- search result ranking;
- query suggestions;
- typeahead;
- related searches;
- semantic search ranking.

Core problem:

- satisfy user intent with high precision while avoiding position bias and ambiguous intent mistakes.

Primary questions:

- Did the ranking better satisfy intent?
- Did users reformulate less?
- Did conversion or successful session improve?
- Did position/layout changes explain the effect?

Representative metrics:

- successful search sessions;
- click quality;
- reformulation rate;
- zero-result rate;
- dwell quality;
- downstream conversion;
- abandonment rate;
- interleaving preference;
- query-segment performance.

---

### 2.6 Ads / Sponsored Recommendation Surfaces

Examples:

- sponsored products;
- retail media recommendations;
- ad recommendations;
- promoted content.

Core problem:

- balance user relevance, advertiser/seller value, and platform revenue.

Primary questions:

- Are ad recommendations incremental?
- Is advertiser ROI stable?
- Is user fatigue or negative feedback increasing?
- Are organic recommendations being crowded out?

Representative metrics:

- incremental conversions;
- ROAS / advertiser ROI;
- ad revenue per user;
- ad load;
- organic displacement;
- negative feedback;
- user retention;
- advertiser retention.

For ads-heavy cases, also use `ads_experiments.md`.

---

## 3. Recommendation Metric & Incrementality Contract
The Agent must evaluate recommendations using a causal incrementality lens and precise mathematical definitions to prevent "engagement traps".

### 3.1 The Metric Definition Contract
The Agent must use these formulas to audit the quality of observed lifts:
* **Qualified CTR** = `Clicks_with_Dwell_Time > X_seconds / Impressions` (Filters out accidental clicks/clickbait).
* **Satisfied Watch Rate** = `Completed_Watches_without_Immediate_Bounce / Total_Starts`.
* **iCVR (Incremental Conversion Rate)** = `Conversion_Rate(Treated) - Conversion_Rate(Control_No_Recs)` or via long-term holdout.
* **Exposure Gini (Concentration)** = A measure of how much exposure is concentrated in the top 1% of items/creators (0 = perfect equality, 1 = total concentration).
* **NDCG / Recall@K**: Use only as **Offline Diagnostics**; never as a sole launch criterion.

### 3.2 Incrementality and Cannibalization Ledger
A Top DS must distinguish between **Net Growth** and **Re-allocation**. The Agent must audit:
* **Surface Cannibalization**: Did the "For You" feed lift come at the expense of "Search" or "Subscriptions" traffic?
* **Intent Displacement**: Did the recommendation force a click that the user would have made organically via navigation?
* **Net Marketplace Lift** = `(Treated_Gain - Untreated_Side_Loss - Organic_Cannibalization)`.

### 3.3 Recommendation Hierarchy by Business Role
* **Decision Metric**: Durable value such as **28-day Retention**, **Return Rate**, or **Satisfied Session Success**.
* **Guardrail Metrics**: **Negative Feedback (Hide/Report)**, **Diversity Decay**, **Latency**, and **Refund/Return Rate** (for e-commerce).
* **Ecosystem Metrics**: **Catalog Coverage**, **New Creator Success Rate**, and **Long-tail Exposure Gini**.
* **Infrastructure Guardrails**: **Serving Latency (P99)** and **Model Inference Error Rate**.

---

## 4. Required Agent Reasoning Order

For every recommendation experiment, the Agent should reason in this order.

### Step 1: Identify Surface and Intervention

Identify:

- recommendation surface;
- user context;
- item/content/seller pool;
- candidate-generation change;
- ranking change;
- reranking/blending change;
- filtering/safety change;
- UI/presentation change;
- exploration policy change;
- notification or distribution change.

### Step 2: Define the Durable Objective

State what the recommender should optimize.

Examples:

- help users find videos they want and are satisfied with;
- increase incremental high-quality purchases;
- improve music discovery without reducing long-term diversity;
- improve marketplace matching without harming seller health;
- improve feed relevance without increasing low-quality engagement.

### Step 3: Classify Metrics

Classify all metrics as:

- offline diagnostic;
- online behavioral;
- decision metric;
- guardrail;
- ecosystem metric;
- mechanism metric.

### Step 4: Validate Experiment Trustworthiness

Before interpreting lifts, check:

- SRM;
- assignment and exposure logging;
- consistent eligibility;
- stable traffic allocation;
- logging completeness;
- treatment/control serving errors;
- latency differences;
- client version balance;
- platform balance;
- bot/spam imbalance;
- metric maturity;
- novelty or seasonality effects.

If telemetry is unreliable, use `do_not_trust_result`.

### Step 5: Check Exposure and Position Bias

Ask:

- Did treatment change what items were shown?
- Did treatment change item position?
- Did layout, card size, autoplay, or slot count change?
- Is CTR lift caused by better ranking or more prominent exposure?
- Did the candidate pool change?
- Is offline evaluation biased by historical exposure?

### Step 5.1: Recommendation Diagnosis Tree
If a core metric fails or shows unexpected lift, trace the "Why":
* **If CTR is up but Retention is down**: Check `Clickbait Score` -> `Diversity Collapse` -> `Novelty Decay` -> `Negative Feedback/Fatigue`.
* **If Offline NDCG is up but Online is flat**: Check `Exposure Bias in Logs` -> `Train/Serve Skew` -> `Candidate Generation Mismatch` -> `Feature Freshness`.
* **If Revenue is up but Margin is down**: Check `Low-Margin Item Bias` -> `Return/Refund Rate` -> `Promotion Dependence`.

### Step 5.2: Semantic and Intent Coherence
Top DS must evaluate the "meaning" of recommendations, not just the numbers:
* **Interest Drift**: Did the model over-react to a single accidental click, narrowing the user's feed too fast?
* **Contextual Fit**: Does the recommendation make sense given the user's current session intent? (e.g., recommending a blender after they just bought one).

### Step 6: Evaluate Short-Term vs Long-Term Value

Ask:

- Did CTR/watch time increase because of real value or stimulation?
- Did saves, completion, return, satisfaction, and repeat behavior improve?
- Did negative feedback, churn, fatigue, or low-quality exposure worsen?
- Is the result mature enough to evaluate retention?

### Step 7: Check Diversity, Novelty, and Coverage

Ask:

- Did recommendations become more repetitive?
- Did catalog or creator coverage decline?
- Did long-tail exposure collapse?
- Did users discover new valuable content/items?
- Did the model increase popularity bias?

### Step 8: Check Supply-Side and Ecosystem Effects

Ask:

- Who gained exposure?
- Who lost exposure?
- Did creator/seller retention change?
- Did new or long-tail items lose opportunity?
- Did the model create perverse incentives for low-quality content?

### Step 9: Analyze Segments

Check:

- new vs existing users;
- cold-start vs warm-start users;
- high-frequency vs low-frequency users;
- niche-interest vs mainstream users;
- geography;
- language;
- platform;
- age or safety-sensitive cohorts if relevant;
- content categories;
- creator/seller tiers;
- head vs torso vs long-tail items.

### Step 10: Choose a Decision Label

Choose exactly one:

- `recommend_launch`
- `launch_with_monitoring`
- `partial_rollout`
- `investigate_further`
- `do_not_launch`
- `do_not_trust_result`
- `use_interleaving_or_counterfactual_eval`
- `use_long_term_holdout`

---

## 5. Decision Labels

Use exactly one primary decision label.

### 5.1 `recommend_launch`

Use when:

- experiment validity checks pass;
- decision metric improves by a meaningful amount;
- online behavior indicates real user value;
- key guardrails are stable or within tolerance;
- negative feedback does not worsen materially;
- diversity, coverage, and ecosystem metrics remain acceptable;
- no important user or supply segment is harmed;
- long-term risk is low or already measured;
- implementation and rollback are ready.

Do not use this label only because CTR or offline NDCG improved.

### 5.2 `launch_with_monitoring`

Use when:

- broad launch is reasonable;
- primary evidence is positive;
- guardrail movement is within tolerance;
- some long-term, diversity, or supply-side risk remains;
- the change is reversible;
- monitoring and rollback thresholds are defined.

### 5.3 `partial_rollout`

Use when:

- benefit is concentrated in a specific user segment, surface, content category, market, or platform;
- broad launch may harm cold-start, niche-interest, long-tail, creator, seller, or sensitive segments;
- evidence is promising but incomplete;
- the model should be exposed gradually to monitor feedback loops.

The Agent must specify:

- target segment;
- rollout percentage;
- duration;
- monitoring metrics;
- rollback thresholds;
- expansion criteria.

### 5.4 `investigate_further`

Use when:

- CTR/watch time improves but satisfaction or retention is unclear;
- offline and online metrics disagree;
- negative feedback or diversity guardrails are ambiguous;
- position/layout bias may explain the lift;
- segment effects are heterogeneous;
- long-term metrics are not mature;
- mechanism is unclear.

### 5.5 `do_not_launch`

Use when:

- decision metric declines;
- engagement improves but retention, satisfaction, trust, or content quality worsens materially;
- negative feedback exceeds tolerance;
- diversity or coverage collapses;
- creator/seller health deteriorates materially;
- policy or safety exposure increases;
- the model exploits clickbait, addictive loops, or low-quality content;
- short-term gain is not aligned with durable value.

### 5.6 `do_not_trust_result`

Use when:

- SRM, logging, exposure, assignment, eligibility, or telemetry issues invalidate the result;
- treatment/control saw different candidate pools due to bug;
- serving errors or latency differences dominate the result;
- outcome events were logged inconsistently;
- analysis uses treatment-induced exposed-only filtering;
- the result is observational but interpreted causally.

### 5.7 `use_interleaving_or_counterfactual_eval`

Use when:

- ordinary A/B is insensitive or too slow for ranking comparison;
- offline logs are biased by historical exposure;
- exposure randomization is needed;
- position bias is material;
- the system needs counterfactual policy evaluation;
- search/ranking quality should be compared at query or session level.

Possible methods:

- team-draft interleaving;
- balanced interleaving;
- randomized exploration bucket;
- inverse propensity scoring;
- doubly robust estimation;
- counterfactual logging;
- query-level or session-level randomization.

### 5.8 `use_long_term_holdout`

Use when:

- short-term metrics are positive but long-term fatigue, retention, trust, diversity, or ecosystem risk is material;
- feedback loops may change future content supply;
- the model changes core feed/ranking behavior;
- the change may create habit, addiction, or creator-incentive effects;
- long-term decision metrics are not mature.

---

## 6. Offline vs Online Evaluation

### 6.1 Offline Metrics Are Pre-Launch Filters

Offline evaluation should answer:

- Is the model technically promising?
- Does it improve ranking quality on held-out logs?
- Does it improve candidate recall?
- Does it improve calibration?
- Does it preserve diversity and coverage?
- Does it avoid regressions for known segments?

Offline metrics should not answer:

- Should we launch broadly?
- Did user satisfaction improve?
- Did long-term retention improve?
- Did supply-side ecosystem improve?

### 6.2 Offline-Online Gap

Offline improvements may fail online because of:

- historical exposure bias;
- popularity bias;
- position bias;
- stale labels;
- train/serve skew;
- candidate generation mismatch;
- feature freshness issues;
- delayed feedback;
- label leakage;
- objective mismatch;
- exploration gap;
- distribution shift;
- UI or product context changes.

Agent Action:

- If offline metrics improve but online metrics are flat or negative, diagnose the offline-online gap before recommending launch.
- If online metrics improve but offline metrics worsen, check whether the online metric reflects durable value or artifact.

---

## 7. Exposure Bias and Counterfactual Evaluation

Recommendation logs are biased because the old recommender decided what users saw.

A missing click is not always a dislike. It may mean the item was never shown.

### 7.1 Key Biases

- **Exposure bias**: users can only interact with exposed items.
- **Position bias**: higher-ranked items receive more attention independent of relevance.
- **Popularity bias**: popular items get more exposure and therefore more data.
- **Feedback-loop bias**: recommendations create future training data that reinforce themselves.
- **Selection bias**: only engaged users or exposed sessions enter the dataset.
- **Survivorship bias**: failed or suppressed items receive little future measurement.

### 7.2 Agent Action

The Agent must ask:

- Was exposure logged?
- Were propensities logged?
- Was there an exploration bucket?
- Were impressions randomized anywhere?
- Was counterfactual evaluation used?
- Are offline metrics corrected for exposure or position?
- Are new items and long-tail items evaluated fairly?

If counterfactual validity is missing and the launch decision depends on offline evaluation, recommend `use_interleaving_or_counterfactual_eval`.

---

## 8. Short-Term Engagement Trap

Short-term engagement can be harmful.

A recommendation model may increase CTR or watch time by recommending:

- clickbait;
- polarizing content;
- overly familiar content;
- repetitive content;
- addictive loops;
- low-quality but attention-grabbing items;
- already-popular items;
- content that users regret consuming;
- products with high return/refund risk.

Agent must check:

- satisfaction surveys;
- save/share/follow quality;
- completion quality;
- post-session return;
- hide/report/not-interested;
- churn;
- topic fatigue;
- content quality;
- trust and safety;
- long-term retention.

Bad reasoning:

> Watch time increased, so the model is better.

Better reasoning:

> Watch time increased, but the Agent must check whether satisfaction, return behavior, negative feedback, content diversity, and long-term retention also support the change.

---

## 9. Diversity, Novelty, Serendipity, and Coverage

Recommendation quality is not only accuracy.

### 9.1 Diversity

Diversity measures whether the recommendation slate provides varied items.

Metrics:

- intra-list diversity;
- category diversity;
- genre diversity;
- creator diversity;
- seller diversity;
- embedding-space diversity;
- repeated-item rate.

### 9.2 Novelty

Novelty measures whether the user sees items outside their already-known exposure.

Metrics:

- new item exposure;
- first-time creator exposure;
- new category exploration;
- long-tail item exposure;
- non-repeat recommendation share.

### 9.3 Serendipity

Serendipity measures valuable surprise.

Metrics:

- unexpected but consumed recommendations;
- new creator followed after recommendation;
- saved/liked novel item;
- repeat engagement with discovered item;
- survey-based discovery satisfaction.

### 9.4 Coverage

Coverage measures how much of the catalog or supply receives meaningful opportunity.

Metrics:

- catalog coverage;
- creator coverage;
- seller/listing coverage;
- long-tail exposure;
- new item first-success rate;
- exposure Gini.

Agent Action:

- If accuracy or CTR improves while diversity, novelty, or coverage deteriorates materially, do not recommend broad launch without explicit tradeoff analysis.
- If discovery is a core product goal, diversity and novelty should be part of the decision metric, not only guardrails.

---

## 10. User Satisfaction and Negative Feedback

Recommendation systems must learn from positive and negative signals.

### 10.1 Positive Signals

Examples:

- completion;
- save/add-to-library;
- share;
- follow/subscribe;
- replay;
- repeat purchase;
- add to wishlist;
- post-session return;
- positive survey response.

### 10.2 Negative Signals

Examples:

- skip;
- hide;
- report;
- not interested;
- dislike;
- unsubscribe;
- mute;
- block;
- refund;
- return;
- fast abandonment;
- rage click;
- complaint;
- churn.

Agent Action:

- Do not treat all engagement as positive.
- Weight negative feedback heavily when the product surface affects trust, safety, or fatigue.
- Check whether negative feedback increased among high-value or sensitive segments.

---

## 11. Creator, Seller, and Supply-Side Health

Recommendation models allocate exposure.

A user-side improvement can harm the supply side.

The Agent must check:

- exposure distribution;
- creator/seller coverage;
- new creator/seller success;
- long-tail exposure;
- creator/seller retention;
- creator/seller earnings;
- content production incentives;
- content quality distribution;
- seller/listing sell-through;
- exposure concentration;
- head-item dominance.

Agent Action:

- If user engagement improves but exposure becomes more concentrated, require ecosystem risk analysis.
- If creator/seller retention or earnings decline materially, do not recommend broad launch without business justification.
- If the surface is marketplace-like, use `marketplace_metrics.md`.

---

## 12. Position, Layout, and Surface Bias Checks

Metric movement may come from presentation changes, not recommendation quality.

Check whether treatment changed:

- item position;
- slot count;
- card size;
- image aspect ratio;
- autoplay;
- preview length;
- title/thumbnail;
- page load order;
- notification prominence;
- scroll behavior;
- default selection;
- recommendation surface traffic mix.

Agent Action:

- If model and UI changed together, separate ranking effect from presentation effect.
- If slot count increased, evaluate per-slot and per-user outcomes.
- If position changed, use position-normalized metrics or interleaving where appropriate.
- If autoplay changed, do not interpret watch time as pure preference.

---

## 13. Recommendation Experiment Design Rules

The Agent must match experimental design to recommendation risk.

| Intervention Type | Common Design | Main Risk | Better Design When Risk Is High |
|---|---|---|---|
| Candidate generation | user-level A/B | recall changes and cold-start effects | exploration bucket + long-term holdout |
| Ranking model | user/session A/B | position bias, engagement trap | A/B + interleaving + satisfaction guardrails |
| Search ranking | query/session A/B | query mix and position bias | interleaving or query-level randomization |
| Feed ranking | user-level A/B | fatigue, content ecosystem effects | long-term holdout + creator exposure monitoring |
| Homepage recommendations | user-level A/B | surface mix and novelty effects | user-level A/B + cohort analysis |
| Product recommendations | user/session A/B | substitution, return/margin risk | incrementality and margin-adjusted metrics |
| Marketplace recommendations | user/seller/listing A/B | supply-side spillover | cluster or market-level experiment |
| Creator recommendations | user-level A/B | exposure concentration | ecosystem monitoring + long-term holdout |
| Notifications | user-level A/B | fatigue and opt-outs | frequency-capped experiment + long-term guardrails |
| Safety filtering | policy cohort / A/B when safe | false positives and trust | staged rollout + audit review |

---

## 14. Interleaving, Bandits, Exploration, and Holdouts

### 14.1 Interleaving

Use interleaving when:

- two ranking systems need sensitive comparison;
- query/session-level preference is more informative than broad user-level outcome;
- position bias must be controlled;
- online A/B would require too much traffic.

Interleaving is especially useful for search and ranked result comparison, but it usually measures short-term preference and should not replace long-term launch guardrails.

### 14.2 Contextual Bandits and Exploration

Use exploration or bandits when:

- the system needs to learn from uncertain recommendations;
- new items or long-tail items need opportunity;
- static exploitation causes feedback loops;
- personalized slates require exploration-exploitation tradeoffs.

Agent must check:

- exploration cost;
- user harm from poor exploration;
- logged propensities;
- fairness to cold-start items;
- long-term learning value.

### 14.3 Long-Term Holdouts

Use long-term holdouts when:

- the model changes a core ranking surface;
- short-term engagement may conflict with retention;
- user fatigue is likely;
- creator/seller incentives may shift;
- content diversity may degrade slowly;
- the model affects future training data.

### 14.4 Feedback Loop and Data Poisoning Audit
A top-tier Agent must recognize when a model is "eating its own tail."

* **Popularity Trap**: Check if the model is over-indexing on head items because they have the most historical data, creating a "winner-take-all" collapse.
* **Data Refresh Bias**: Is the model learning from its own bias because the "Treatment" group controls 100% of the UI exposure?
* **Self-Fulfilling Prophecy**: The model predicts an item is good -> puts it at Position 1 -> user clicks because of position -> model thinks its prediction was right.
* **Audit Action**: Use **Randomized Exploration Buckets** (5% traffic) to collect unbiased feedback for future model training.

---
## 15. Segment and Cohort Analysis

Averages hide recommendation harm.

Required scans:

- new vs existing users;
- cold-start vs warm-start users;
- high-frequency vs low-frequency users;
- niche-interest vs mainstream users;
- high-value vs low-value users;
- subscribed vs free users;
- geography;
- language;
- platform;
- acquisition channel;
- content category;
- creator/seller tier;
- head vs long-tail items;
- safety-sensitive cohorts when relevant.

Interpretation rules:

- Do not overreact to noisy tiny segments.
- Prioritize segments central to product strategy or risk.
- If cold-start or niche-interest users are harmed, broad launch may degrade discovery quality.
- If long-tail or new creator/seller exposure is harmed, check supply-side effects.

---

## 16. Metric Maturity and Long-Term Risk

Recommendation metrics mature at different speeds.

### 16.1 Fast Metrics

Examples:

- impressions;
- CTR;
- starts;
- skips;
- first-click latency;
- feed load latency;
- click depth.

Fast metrics are useful for debugging but rarely sufficient for launch.

### 16.2 Medium-Lag Metrics

Examples:

- completion;
- save/add-to-library;
- add-to-cart;
- purchase;
- refund;
- hide/report;
- successful session;
- post-session return.

### 16.3 Long-Lag Metrics

Examples:

- 7-day and 28-day retention;
- long-term satisfaction;
- LTV;
- repeat purchase;
- subscription churn;
- creator/seller retention;
- content ecosystem quality;
- diversity decay;
- trust erosion;
- fatigue.

Agent Action:

- Mark unavailable long-lag evidence as `not_mature_yet`.
- Do not recommend broad launch for high-risk core ranking changes when long-term metrics are not mature.
- Consider `use_long_term_holdout` when short-term metrics are positive but long-term risk is material.

---

## 17. Guardrail and Non-Inferiority Logic

Recommendation guardrails often need non-inferiority logic.

The question is not always:

> Did the guardrail improve?

The better question is:

> Did the guardrail deteriorate beyond acceptable tolerance?

Examples:

- hide/report rate must not increase by more than 0.1 percentage points;
- 7-day retention must not decline by more than 0.2 percentage points;
- creator exposure Gini must not increase beyond threshold;
- long-tail coverage must not decline by more than 1%;
- recommendation latency must not increase beyond 20 ms;
- refund rate must not increase by more than 0.2 percentage points;
- negative survey satisfaction must not increase materially.

Agent Action:

- If guardrail deterioration exceeds tolerance, prefer `do_not_launch` or `investigate_further`.
- If guardrail deterioration is small, within tolerance, and reversible, consider `launch_with_monitoring`.
- For core feed/ranking changes, require stricter long-term guardrails.

---

## 18. Recommendation Failure Diagnosis Tree

### 18.1 CTR Increased

Check:

- position or layout change;
- thumbnail/title changes;
- accidental clicks;
- repeated exposure;
- clickbait;
- low-quality clicks;
- downstream completion;
- negative feedback;
- retention.

Possible interpretation:

- healthy if click quality, satisfaction, and retention improve;
- suspicious if negative feedback or abandonment rises.

### 18.2 Watch Time Increased

Check:

- completion quality;
- satisfaction;
- fatigue;
- repeated content;
- autoplay;
- next-day return;
- long-term retention;
- content quality.

Possible interpretation:

- healthy if satisfied watch time and return improve;
- unhealthy if users watch more but report/hide/churn more.

### 18.3 Offline NDCG Improved but Online Metrics Did Not

Check:

- exposure bias;
- train/serve skew;
- stale labels;
- candidate recall;
- feature freshness;
- objective mismatch;
- segment regressions;
- cold-start performance.

Possible interpretation:

- model may be better on historical logs but not better for users.

### 18.4 Conversion Increased

Check:

- margin;
- returns/refunds;
- repeat purchase;
- substitution;
- seller exposure;
- recommendation cannibalization;
- product quality.

Possible interpretation:

- healthy if incremental margin-adjusted value improves;
- suspicious if high-return or low-margin products drive lift.

### 18.5 Diversity Declined

Check:

- popularity bias;
- head-content overexposure;
- category concentration;
- user fatigue;
- long-tail supply health;
- new item discovery.

Possible interpretation:

- may be acceptable only if durable value improves and diversity remains within tolerance.

### 18.6 Negative Feedback Increased

Check:

- content safety;
- repetitive recommendations;
- irrelevant personalization;
- over-notification;
- bad cold-start inference;
- platform or cohort concentration.

Possible interpretation:

- do not launch broadly if negative feedback exceeds tolerance.

---

## 19. Decision Matrix

| Evidence Pattern | Recommended Decision |
|---|---|
| Decision metric improves, satisfaction/retention stable or better, guardrails stable, diversity acceptable | `recommend_launch` |
| Decision metric improves, guardrails within tolerance, long-term risk manageable | `launch_with_monitoring` |
| Benefit concentrated in specific user/content/category segments | `partial_rollout` |
| CTR improves but completion, satisfaction, or retention unclear | `investigate_further` |
| Offline metrics improve but online decision metrics are flat/negative | `investigate_further` |
| CTR/watch time improves but hide/report/churn worsens materially | `do_not_launch` |
| Engagement improves but diversity/coverage collapses | `investigate_further` or `do_not_launch` |
| User metrics improve but creator/seller exposure concentration worsens materially | `investigate_further` or `partial_rollout` |
| Historical logs are biased and no counterfactual exposure data exists | `use_interleaving_or_counterfactual_eval` |
| Core feed/ranking change has positive short-term metrics but long-term risk is unknown | `use_long_term_holdout` |
| SRM, logging, exposure, or assignment failure exists | `do_not_trust_result` |
| Recommendation latency or serving errors increase materially | `do_not_launch` or `investigate_further` |
| Product recommendations increase purchases but returns/refunds/margin worsen | `investigate_further` or `do_not_launch` |

---

## Quantitative Decision Benchmarks
* **Pattern 1**: CTR +5%, Watch Time +8%, Dislike/Hide +15%, Retention -1% => `do_not_launch` (Exploitative engagement/Clickbait).
* **Pattern 2**: Offline NDCG +2%, Online Engagement +0.2%, Exposure Gini +10%, New-Item Success -5% => `investigate_further` (Popularity bias/Ecosystem risk).
* **Pattern 3**: Conversion +4%, Refund Rate +1.5pp (above tolerance), Net Margin -2% => `do_not_launch` (Low-quality commerce matching).

---
## 20. Minimum Evidence Required for Recommendation Experiment Review

A recommendation experiment review should include:

### 20.1 Product Context

- recommendation surface;
- user context;
- item/content/supply pool;
- model or product change;
- decision being made;
- reversibility;
- risk tier.

### 20.2 Experiment Design

- randomization unit;
- exposure definition;
- treatment and control;
- candidate generation changes;
- ranking/reranking changes;
- UI/presentation changes;
- duration;
- traffic allocation;
- sample size;
- metric maturity;
- pre-specified launch criteria.

### 20.3 Metric Hierarchy

- offline diagnostics;
- online behavioral metrics;
- decision metric;
- guardrails;
- diversity/novelty/coverage metrics;
- supply-side metrics;
- long-term metrics.

### 20.4 Results

- metric movement;
- practical magnitude;
- confidence intervals;
- segment effects;
- guardrail movement;
- diversity and coverage movement;
- negative feedback;
- latency and serving health;
- long-term readout if available.

### 20.5 Bias and Validity Checks

- SRM;
- exposure logging;
- position bias;
- UI/layout changes;
- train/serve skew;
- candidate pool changes;
- telemetry consistency;
- novelty/seasonality;
- counterfactual validity;
- interference risk.

### 20.6 Recommendation

- decision label;
- evidence summary;
- risks;
- missing evidence;
- next analysis;
- rollout or holdout plan;
- rollback thresholds.

---

## 21. Response Template for the Agent

Use this structure when answering a recommendation experiment question.

```text
Decision: [recommend_launch / launch_with_monitoring / partial_rollout / investigate_further / do_not_launch / do_not_trust_result / use_interleaving_or_counterfactual_eval / use_long_term_holdout]

Recommendation surface:
[feed / video/audio / ecommerce / marketplace / search / ads / other]

Decision problem:
[Restate the recommendation decision.]

Metric hierarchy:
- Offline diagnostics:
- Online behavioral metrics:
- Decision metric:
- Guardrails:
- Diversity/novelty/coverage:
- Supply-side/ecosystem metrics:
- Long-term metrics:

Experiment trustworthiness:
[SRM, assignment, exposure, telemetry, serving health.]

Bias checks:
- Exposure bias:
- Position/layout bias:
- Candidate pool changes:
- Train/serve skew:
- Counterfactual validity:

Evidence assessment:
1. Durable user value:
2. Short-term engagement quality:
3. Negative feedback:
4. Diversity and discovery:
5. Supply-side/ecosystem effects:
6. Segment heterogeneity:
7. Long-term risk:

Reliable interpretation:
[What can and cannot be concluded.]

Missing evidence:
- [Evidence 1]
- [Evidence 2]
- [Evidence 3]

Next steps:
- [Analysis or experiment step]
- [Rollout/holdout/monitoring step]
- [Rollback threshold]
```

---

## 22. Evaluation Criteria for Agent Answers

A high-quality Agent answer should:

- identify the recommendation surface;
- define a durable recommendation objective;
- separate offline metrics from online and decision metrics;
- avoid treating CTR, watch time, or offline NDCG as sufficient;
- check experiment validity before interpreting results;
- check exposure bias and position/layout bias;
- evaluate short-term engagement quality;
- check negative feedback and satisfaction;
- analyze diversity, novelty, serendipity, and coverage;
- consider creator/seller/supply-side effects;
- analyze segments and cold-start users;
- consider long-term fatigue and feedback loops;
- select exactly one decision label;
- state missing evidence and next steps.

Penalize an answer if it:

- recommends launch because CTR increased;
- recommends launch because offline NDCG improved;
- ignores satisfaction and negative feedback;
- ignores diversity and coverage;
- ignores creator/seller/supply-side effects;
- ignores position or UI changes;
- ignores exposure bias in offline evaluation;
- ignores long-term retention and fatigue;
- treats raw watch time as always good;
- gives generic recommendation-system advice without a decision label;
- recommends partial rollout without target segment, monitoring, and expansion criteria.

---

## 23. Common Failure Modes

The Agent should avoid these failure modes:

1. **CTR absolutism**

   Treating clicks as proof of recommendation quality.

2. **Offline metric overtrust**

   Treating NDCG, Recall@K, or AUC as launch evidence without online validation.

3. **Watch-time bias**

   Treating longer consumption as always good, even when satisfaction or retention declines.

4. **Ignoring negative feedback**

   Failing to check hides, reports, skips, dislikes, unsubscribes, returns, refunds, or churn.

5. **Ignoring diversity**

   Letting the model collapse into popularity bias or repetitive recommendations.

6. **Ignoring supply-side allocation**

   Improving user metrics while harming creators, sellers, or long-tail items.

7. **Ignoring exposure bias**

   Evaluating the recommender only on logs created by the old recommender.

8. **Ignoring position and layout bias**

   Mistaking UI prominence for model quality.

9. **Ignoring long-term risk**

   Launching based on short-term metrics before fatigue, retention, or ecosystem effects mature.

10. **Ignoring cold-start and niche users**

   Optimizing average performance while harming users or items with sparse history.

---

## 24. Final Rule

The Agent should optimize for durable recommendation value, not surface engagement.

A recommendation change is successful only if it improves the user's ability to discover valuable content, products, people, or actions while preserving satisfaction, trust, diversity, supply-side incentives, and long-term retention.

If the Agent cannot explain whether the lift reflects real value, biased exposure, UI position effects, short-term stimulation, or ecosystem redistribution, it should not recommend broad launch.

The best recommendation-experiment answer should feel like a senior recommendation data scientist reviewing a launch decision, not like a dashboard report saying CTR went up.

---

## External Methodology References

These references are included to help future maintainers understand the methodological background behind this playbook.

- YouTube Help, "YouTube's Recommendation System."
- YouTube Official Blog, "On YouTube's recommendation system."
- Netflix Technology Blog, "Netflix Recommendations: Beyond the 5 stars."
- Netflix Technology Blog, "It's All A/Bout Testing: The Netflix Experimentation Platform."
- Netflix Research, "Experimentation and Causal Inference."
- Spotify Research, "Understanding and Evaluating User Satisfaction with Music Discovery."
- Spotify Research, "User Intents and Satisfaction with Slate Recommendations."
- Spotify Research, "Optimizing Audio Recommendations for the Long-Term."
- Kaminskas and Bridge, "Diversity, Serendipity, Novelty, and Coverage: A Survey and Empirical Analysis of Beyond-Accuracy Objectives in Recommender Systems."
- Holtz et al., "The Engagement-Diversity Connection: Evidence from a Field Experiment on Spotify."
- Covington et al., "Deep Neural Networks for YouTube Recommendations."
