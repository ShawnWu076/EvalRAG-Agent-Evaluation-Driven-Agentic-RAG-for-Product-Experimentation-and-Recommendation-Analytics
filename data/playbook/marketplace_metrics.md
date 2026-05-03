# Marketplace Metrics Playbook

This playbook defines how an Agent should reason about marketplace metrics, marketplace experiments, and marketplace launch decisions.

It is designed for an evaluation-driven Agentic RAG system. The goal is not to make the Agent list common marketplace KPIs. The goal is to make the Agent behave like a senior data scientist who can diagnose whether a marketplace intervention improves durable matching efficiency without damaging liquidity, trust, economics, or ecosystem balance.

A marketplace is not a single-sided product funnel. It is a system of interacting participants. A metric improvement for one side may impose hidden costs on another side. A buyer conversion lift can reduce seller earnings. A seller pricing tool can change buyer demand allocation. A ranking change can increase short-term GMV while concentrating exposure among a few sellers and weakening long-tail supply. A subsidy can increase transactions while destroying contribution margin.

The Agent should treat marketplace growth as real only when it improves durable matching efficiency for both sides of the marketplace while preserving trust, unit economics, and ecosystem health.

---

## Quick Retrieval Summary

Use this playbook when the user asks about marketplace metrics, marketplace health, supply-demand balance, buyer-seller matching, GMV growth, liquidity, marketplace experiments, marketplace ranking, pricing, subsidies, search-to-fill, seller retention, marketplace interference, or whether a marketplace product change should launch.

This playbook is especially relevant when:

- GMV, orders, bookings, or completed transactions increase;
- buyer conversion improves but seller-side metrics worsen;
- seller tools, pricing recommendations, ranking, search, ads, incentives, or subsidies change;
- supply and demand may be imbalanced by geography, category, time, price band, or inventory segment;
- treatment effects may spill over across buyers, sellers, listings, markets, or time windows;
- ordinary user-level A/B testing may be biased by marketplace interference;
- the user asks whether marketplace growth is healthy or sustainable;
- local markets behave differently from aggregate results;
- a metric lift may be caused by subsidy, concentration, cannibalization, or low-quality matching.

Default reasoning order:

1. Identify the marketplace type.
2. Define the marketplace objective and metric hierarchy.
3. Diagnose liquidity on both demand and supply sides.
4. Evaluate match quality, not only match quantity.
5. Check buyer health, seller health, and platform economics.
6. Scan local markets, segments, categories, and cohorts.
7. Check concentration, fairness, and ecosystem risk.
8. Evaluate interference and experimental design validity.
9. Convert evidence into a marketplace decision label.
10. State missing evidence and next analysis.

---

## 1. Core Principle

Marketplace growth is only healthy if it improves durable matching efficiency without degrading trust, economics, or ecosystem balance.

The Agent should not treat GMV, orders, bookings, clicks, or conversion as sufficient evidence of marketplace health.

A good marketplace decision depends on:

- whether demand can find enough relevant supply;
- whether supply receives enough valuable demand;
- whether matches complete successfully;
- whether match quality is improving;
- whether both sides retain;
- whether unit economics are sustainable;
- whether growth is local-market healthy rather than aggregate-only;
- whether exposure and earnings are not becoming destructively concentrated;
- whether trust, safety, fraud, refunds, and support burden remain controlled;
- whether the experiment design accounts for interference and network effects.

The Agent should avoid two common mistakes:

- **single-sided optimization**: optimizing buyer conversion while ignoring seller health;
- **surface growth bias**: treating higher GMV or transaction count as healthy without checking match quality, margin, and ecosystem effects.

---

## 2. Marketplace Types

The Agent must classify the marketplace before selecting metrics.

Different marketplaces require different OECs, guardrails, and experimental designs.

### 2.1 Instant Matching Marketplace

Examples:

- rideshare;
- food delivery;
- courier dispatch;
- local services with urgent demand;
- on-demand labor.

Core problem:

- match real-time demand with available supply under time, distance, and capacity constraints.

Primary marketplace questions:

- Can demand be served quickly?
- Is supply underused or overloaded?
- Are wait times acceptable?
- Are providers earning enough?
- Are cancellations controlled?
- Is the system balanced by time and location?

Representative metrics:

- request-to-match rate;
- request-to-complete rate;
- ETA;
- wait time;
- cancellation rate;
- supply utilization;
- provider earnings per active hour;
- idle time;
- completed trips/orders per active supply hour.

---

### 2.2 Inventory Booking Marketplace

Examples:

- travel lodging;
- short-term rentals;
- ticketing;
- reservations;
- appointment booking.

Core problem:

- match demand intent with finite inventory across date, location, price, and quality constraints.

Primary marketplace questions:

- Can users find bookable inventory?
- Are hosts or suppliers earning enough?
- Is inventory availability broad enough?
- Are cancellations, refunds, and quality issues controlled?
- Is the marketplace balanced by geography and date?

Representative metrics:

- search-to-book rate;
- availability rate;
- booking conversion;
- occupancy;
- nights booked;
- host earnings;
- host retention;
- cancellation rate;
- refund rate;
- guest rating;
- time-to-book;
- rejected request rate.

---

### 2.3 Listing Commerce Marketplace

Examples:

- ecommerce marketplace;
- resale marketplace;
- handmade goods marketplace;
- B2B product marketplace.

Core problem:

- help buyers discover relevant listings and help sellers convert supply into sales.

Primary marketplace questions:

- Can buyers find relevant products?
- Are listings high-quality and available?
- Are sellers getting enough demand?
- Are refunds, returns, fraud, and shipping issues controlled?
- Is exposure distributed sustainably?

Representative metrics:

- search-to-purchase rate;
- listing view-to-purchase;
- sell-through rate;
- inventory turnover;
- seller activation;
- first sale time;
- repeat buyer rate;
- repeat seller rate;
- refund/return rate;
- shipping defect rate;
- seller response time;
- listing quality score.

---

### 2.4 Labor or Services Marketplace

Examples:

- freelance marketplace;
- tutoring marketplace;
- care marketplace;
- home services marketplace.

Core problem:

- match buyer demand with qualified providers while protecting trust, quality, and long-term supply.

Primary marketplace questions:

- Are buyers matched with qualified providers?
- Are providers earning enough and staying active?
- Is service quality high?
- Are cancellations, disputes, and safety events controlled?

Representative metrics:

- request-to-hire rate;
- proposal response rate;
- job completion rate;
- provider earnings;
- provider retention;
- buyer repeat rate;
- dispute rate;
- safety incident rate;
- time-to-first-response;
- time-to-complete.

---

### 2.5 Creator, Content, or Attention Marketplace

Examples:

- creator platforms;
- social feeds;
- short-video platforms;
- recommendation ecosystems.

Core problem:

- allocate attention between consumers and creators without degrading content quality, creator incentives, or user trust.

Primary marketplace questions:

- Are users receiving valuable content?
- Are creators receiving fair and motivating distribution?
- Is content quality improving or degrading?
- Is the platform avoiding low-quality engagement traps?

Representative metrics:

- qualified engagement;
- creator retention;
- creator posting rate;
- creator earnings;
- exposure concentration;
- content diversity;
- report/hide rate;
- follow/repeat engagement;
- low-quality content exposure;
- long-term user retention.

---

### 2.6 Ads Marketplace

Examples:

- sponsored search;
- display ads;
- retail media;
- promoted listings.

Core problem:

- allocate impressions between users, advertisers, and platform revenue while preserving advertiser ROI and user experience.

Primary marketplace questions:

- Are advertisers getting incremental value?
- Are users harmed by ad load or low relevance?
- Is short-term revenue hurting long-term advertiser or user retention?
- Is the auction efficient and fair?

Representative metrics:

- incremental conversions;
- advertiser ROI / ROAS;
- cost per incremental acquisition;
- ad revenue per user;
- ad load;
- negative feedback per user;
- advertiser retention;
- auction density;
- bid landscape health;
- user retention.

For ads marketplace analysis, also use `ads_experiments.md`.

---

## 3. Marketplace Lifecycle and Stage-Aware Metrics
The Agent must adjust the weight of metrics based on the marketplace's current maturity stage.

| Stage | Primary Focus | Critical Metrics | Agent Bias |
|---|---|---|---|
| **Cold Start / Early** | Liquidity & Activation | Match rate, first sale time, seller activation | High tolerance for low margin to build liquidity. |
| **Scaling** | Growth & Retention | GMV, repeat buyer/seller rate, LTV/CAC | Prioritize scale and retention over short-term take rate. |
| **Mature Optimization**| Efficiency & Quality | Quality-adjusted GMV, match quality, support cost | Low tolerance for quality erosion; focus on contribution margin. |
| **Monetization** | Unit Economics | Take rate, net revenue, ad load, subsidy efficiency | Ensure take rate increases do not cause seller churn. |
| **Defensive Quality** | Trust & Ecosystem | Concentration, fraud, long-tail health, brand risk | Protect the ecosystem even if GMV growth is flat. |

### 3.1 North Star / Overall Evaluation Criterion

The OEC should represent durable marketplace value, not surface activity.

Possible OECs:

- quality-adjusted completed transactions;
- successful matches;
- completed bookings with acceptable satisfaction;
- contribution-margin-adjusted GMV;
- retained buyer-seller match value;
- liquidity-adjusted transaction value;
- long-term marketplace value.

Bad OEC:

> Gross GMV.

Better OEC:

> Quality-adjusted completed transactions with stable buyer retention, seller earnings, refund rate, and contribution margin.

### 3.2 Liquidity Metrics

Liquidity measures whether the marketplace can reliably match demand and supply.

Demand-side liquidity:

- search-to-fill rate;
- request-to-match rate;
- request-to-complete rate;
- search-to-purchase;
- search-to-book;
- no-result rate;
- stockout rate;
- time-to-match;
- time-to-book;
- wait time;
- price availability.

Supply-side liquidity:

- sell-through rate;
- occupancy;
- utilization;
- listing conversion;
- first sale time;
- time-to-first-booking;
- provider active hours filled;
- seller demand received;
- idle time;
- supply coverage.

### 3.3 Match Quality Metrics

A match is not successful just because it completed.

Match quality metrics:

- cancellation rate;
- refund rate;
- return rate;
- complaint rate;
- dispute rate;
- rating;
- rebooking rate;
- repeat purchase rate;
- delivery defect rate;
- service defect rate;
- support ticket rate;
- buyer satisfaction;
- seller satisfaction.

* **Price Discovery Efficiency**: The delta between asking price and final transaction price;
* **Price Accuracy**: Rate of price changes or "bait-and-switch" reports after match;
* **Price Transparency**: Buyer/Seller sentiment or complaints regarding hidden fees or surge volatility.

### 3.4 Buyer Health Metrics

Buyer health measures whether the demand side is improving.

Examples:

- buyer activation;
- search-to-intent;
- intent-to-transaction;
- repeat purchase or booking;
- buyer retention;
- buyer LTV;
- failed searches;
- price sensitivity;
- churn;
- complaint rate;
- refund experience;
- trust signals.

### 3.5 Seller / Supply Health Metrics

Seller health measures whether the supply side remains motivated, active, and high-quality.

Examples:

- seller activation;
- first sale / first booking time;
- seller retention;
- seller earnings;
- earnings per active hour;
- exposure received;
- response rate;
- cancellation by seller;
- listing quality;
- inventory availability;
- long-tail seller success;
- seller churn;
- seller NPS or satisfaction.

### 3.6 Platform Economics Metrics

Platform economics determine whether growth is financially sustainable.

Examples:

- take rate;
- net revenue;
- contribution margin;
- gross margin;
- subsidy per transaction;
- incentive cost;
- CAC payback;
- LTV/CAC;
- refund cost;
- support cost;
- chargeback cost;
- fraud cost;
- promotion dependence.

The Agent should treat GMV as scale, not profit.

### 3.7 Trust, Safety, and Policy Metrics

Marketplaces rely on trust. Growth that damages trust is not healthy.

Examples:

- fraud rate;
- scam reports;
- policy violations;
- chargebacks;
- counterfeit reports;
- unsafe transaction reports;
- identity verification failure;
- review manipulation;
- suspicious account rate;
- account enforcement appeals;
- dispute escalation.

### 3.8 Ecosystem Balance Metrics

Ecosystem metrics protect the marketplace from winner-take-all collapse or local degradation.

Examples:

- exposure concentration;
- GMV concentration;
- seller earnings Gini;
- top seller share;
- long-tail seller success;
- category diversity;
- geography coverage;
- price-band coverage;
- supply diversity;
- new seller success rate;
- market-level supply-demand ratio.

---

## 4. Marketplace Metric Definition Contract
To avoid misinterpretation, the Agent must use the following standard formulas:

* **Search-to-Fill** = `successful_filled_searches / qualified_searches`
* **Request-to-Complete** = `completed_transactions / valid_requests`
* **Seller Utilization** = `occupied_or_paid_supply_time / active_supply_time`
* **Take Rate** = `net_revenue / GMV`
* **Contribution Margin per Order** = `(net_revenue - variable_cost - subsidy - support_cost - refund_cost) / orders`
* **Top Seller Share** = `GMV_from_top_X_percent_sellers / total_GMV`
* **Fulfillment Rate** = `completed_orders / total_eligible_orders`

### Step 1: Define the Marketplace

Agent must identify:

- marketplace type;
- sides of the marketplace;
- transaction unit;
- matching mechanism;
- product surface;
- decision being made.

Examples:

- buyer-side search ranking;
- seller-side pricing tool;
- subsidy change;
- marketplace fee change;
- inventory recommendation;
- trust and safety enforcement;
- logistics or dispatch algorithm;
- promoted listing change.

### Step 2: Define the OEC

Agent must define the marketplace OEC and explain why it represents durable value.

Do not use GMV alone unless the user explicitly asks for revenue scale and the Agent states its limitations.

### Step 3: Classify Metrics

Classify each metric as:

- OEC / decision metric;
- liquidity metric;
- match quality metric;
- buyer health metric;
- seller health metric;
- platform economics metric;
- trust and safety metric;
- ecosystem balance metric;
- diagnostic metric.

### Step 4: Diagnose Liquidity

Check both sides:

- demand-side liquidity;
- supply-side liquidity;
- local-market density;
- time-of-day or seasonality effects;
- category or price-band coverage.

### Step 5.1: Marketplace Diagnosis Tree

If a core metric fails, the Agent must trace the root cause:
* **If demand-side conversion is down**: Check `supply availability` -> `price mismatch` -> `ranking relevance` -> `trust/safety issue` -> `checkout friction`.
* **If seller earnings are down**: Check `exposure loss` -> `price pressure` -> `take-rate change` -> `demand shift` -> `concentration increase`.
* **If GMV is up but margin is down**: Check `subsidy intensity` -> `refund/support cost` -> `low-margin category mix` -> `fraud/chargeback`.

### Step 5.2: Price Elasticity and Surplus Framework

* **Buyer/Seller Elasticity**: How do demand and supply volume respond to price/fee changes?
* **Pass-through Rate**: What percentage of a subsidy or fee change is passed to the other side?
* **Surplus Proxy**: Evaluate `consumer surplus` (utility vs. price) and `seller surplus` (earnings vs. effort).
* **Affordability**: Monitor `price fairness complaints` and `price dispersion` across similar listings.

### Step 6: Evaluate Unit Economics

Ask whether growth is profitable or subsidy-driven.

Agent must check:

- net revenue;
- contribution margin;
- incentive cost;
- refund/support/fraud cost;
- CAC payback;
- seller/buyer LTV.

### Step 7: Scan Segments and Local Markets

Marketplace averages often hide local failure.

Check:

- geography;
- category;
- price band;
- time-of-day;
- buyer intent;
- seller cohort;
- listing quality tier;
- supply maturity;
- new vs existing users;
- high-value vs low-value users;
- dense vs sparse markets.

### Step 8: Check Concentration and Ecosystem Risk

Ask whether the change increases concentration or harms long-tail health.

Check:

- top seller share;
- exposure concentration;
- buyer concentration;
- category diversity;
- new seller success;
- long-tail seller retention;
- market coverage.

### Step 9: Check Interference and Network Effects

Ask whether treatment changes outcomes for untreated units.

Interference is likely when the change affects:

- ranking;
- pricing;
- inventory allocation;
- search visibility;
- recommendations;
- subsidies;
- supply incentives;
- buyer consideration sets;
- seller competition;
- auction allocation.

If interference is likely, the Agent should not rely only on ordinary individual-level A/B estimates.

### Step 10: Make a Marketplace Decision

Choose one label:

- `healthy_growth`
- `launch_with_monitoring`
- `partial_rollout`
- `investigate_further`
- `do_not_launch`
- `use_marketplace_level_experiment`
- `do_not_trust_result`

---

## 5. Marketplace Decision Labels

Use exactly one primary marketplace decision label.

### 5.1 `healthy_growth`

Use when:

- OEC improves meaningfully;
- liquidity improves on the relevant side;
- match quality remains stable or improves;
- buyer and seller health are stable;
- platform economics are sustainable;
- trust/safety guardrails are stable;
- no important local market or segment is harmed;
- interference risk is low or properly handled.

### 5.2 `launch_with_monitoring`

Use when:

- marketplace improvement is meaningful;
- guardrails are within tolerance;
- some local-market or long-term risk remains;
- the change is reversible;
- monitoring and rollback thresholds are defined.

### 5.3 `partial_rollout`

Use when:

- benefit is concentrated in specific markets, categories, price bands, or cohorts;
- broad launch may harm some segments;
- interference risk is manageable only at limited scope;
- local density is not yet sufficient everywhere;
- seller or buyer guardrails require controlled expansion.

The Agent must specify:

- target market or segment;
- rollout size;
- duration;
- monitoring metrics;
- rollback thresholds;
- expansion criteria.

### 5.4 `investigate_further`

Use when:

- GMV or transactions increase but match quality is unclear;
- buyer and seller metrics conflict;
- effects differ by geography, category, or cohort;
- unit economics are incomplete;
- concentration risk is possible;
- interference may bias the estimate;
- metric definitions are ambiguous;
- marketplace health cannot be determined from the given metrics.

### 5.5 `do_not_launch`

Use when:

- buyer conversion improves but seller health deteriorates materially;
- transaction count increases but refunds, cancellations, disputes, or support costs rise materially;
- GMV growth is subsidy-driven and contribution margin deteriorates;
- concentration risk harms long-tail supply;
- trust/safety risk increases;
- local markets are harmed;
- long-term marketplace health is likely worse.

### 5.6 `use_marketplace_level_experiment`

Use when:

- individual-level randomization is likely biased by interference;
- treatment affects ranking, pricing, inventory, exposure, or supply competition;
- spillovers are likely between treated and untreated participants;
- local market effects matter;
- marketplace-level counterfactual is required.

Possible designs:

- cluster randomization;
- geo experiment;
- market-level holdout;
- switchback experiment;
- time-based randomization;
- synthetic control;
- difference-in-differences.

### 5.7 `do_not_trust_result`

Use when:

- SRM, assignment failure, exposure imbalance, logging failure, metric inconsistency, or post-treatment filtering invalidates the result;
- marketplace result is observational but interpreted as randomized evidence;
- experiment design cannot identify the marketplace effect.

---

## 6. Liquidity Framework

Liquidity is the ability of a marketplace to produce successful matches between supply and demand.

### 6.1 Demand-Side Liquidity

Demand-side liquidity asks:

> When buyers arrive with intent, can they find suitable supply?

Important metrics:

- search-to-fill;
- request-to-complete;
- search-to-book;
- search-to-purchase;
- no-result rate;
- inventory availability;
- price availability;
- wait time;
- failed search rate;
- checkout failure;
- quote-to-book;
- time-to-match.

Agent Action:

- If demand-side liquidity improves, check whether match quality and seller health remain stable.
- If demand-side liquidity worsens, determine whether the problem is supply shortage, poor ranking, price mismatch, quality mismatch, trust issue, or technical friction.

### 6.2 Supply-Side Liquidity

Supply-side liquidity asks:

> When sellers or providers make supply available, do they receive enough valuable demand?

Important metrics:

- sell-through;
- occupancy;
- utilization;
- listing conversion;
- first sale time;
- seller earnings;
- idle time;
- demand received per seller;
- listing impressions per active seller;
- response burden;
- cancellation rate;
- seller retention.

Agent Action:

- If buyer metrics improve but supply-side liquidity worsens, do not recommend broad launch without deeper analysis.
- If supply-side utilization is too high, check whether demand is being constrained by insufficient supply.
- If utilization is too low, check whether the marketplace has over-supplied or lacks demand density.

### 6.3 Liquidity Is Local

Aggregate liquidity can hide local failure.

Agent must scan:

- geography;
- category;
- time;
- price band;
- supply type;
- demand intent;
- supply maturity;
- buyer cohort;
- seller cohort.

Example:

> Overall search-to-book improves, but sparse cities have higher no-availability rates. This is not broad healthy growth. Consider partial rollout to dense markets only.

---

## 7. Lost Demand and Supply Constraint Adjustment

The Agent must account for unobserved "Lost Demand" that does not reach the checkout stage.
* **No-Result Searches**: High search volume with zero bookable/purchasable results.
* **Abandoned Requests**: Users who drop off due to high ETA, stockouts, or excessive surge pricing.
* **Stockout-Adjusted Conversion**: Estimated conversion rate if all items/slots were available.
* **Lost GMV**: Estimated transaction value lost due to supply shortages or technical friction.

Agent must check:

- completed transaction rate;
- cancellation rate;
- refund or return rate;
- complaint rate;
- dispute rate;
- rating;
- repeat purchase;
- rebooking;
- support ticket rate;
- trust/safety event rate;
- buyer and seller satisfaction.

Bad reasoning:

> Orders increased, so marketplace health improved.

Better reasoning:

> Orders increased, but cancellations and complaints also rose. The result may reflect lower-quality liquidity rather than healthier matching.

---

## 8. Unit Economics Framework

The Agent must distinguish marketplace scale from marketplace economics.

### 8.1 Scale Metrics

Examples:

- GMV;
- orders;
- bookings;
- trips;
- gross transaction value;
- active buyers;
- active sellers.

Scale metrics are useful, but they are not sufficient.

### 8.2 Economic Quality Metrics

Examples:

- net revenue;
- take rate;
- contribution margin;
- subsidy per order;
- incentive cost;
- support cost;
- refund cost;
- chargeback cost;
- fraud cost;
- buyer LTV;
- seller LTV;
- CAC payback.

Agent Action:

- If GMV increases but contribution margin decreases, classify the result as economically ambiguous or unhealthy.
- If transactions increase because subsidy increases, check incremental transactions per subsidy dollar.
- If take rate increases, check seller retention and supply quality.

* **Incremental GMV per Subsidy Dollar (iROI)**: The causal lift in GMV relative to the incremental cost of incentives;
* **Subsidy Efficiency Gini**: Concentration of subsidy spend vs. concentration of incremental value created.

---

## 9. Buyer-Seller Tradeoff Framework

Marketplace interventions often help one side while harming another.

### 9.1 Buyer-Side Wins That May Harm Sellers

Examples:

- lower prices;
- more aggressive discounts;
- ranking that favors cheapest supply;
- stricter cancellation penalties;
- faster delivery expectations;
- search ranking that concentrates demand among top sellers.

Risks:

- lower seller earnings;
- seller churn;
- reduced supply quality;
- lower long-tail participation;
- strategic seller behavior.

### 9.2 Seller-Side Wins That May Harm Buyers

Examples:

- higher prices;
- lower supply requirements;
- easier listing activation;
- seller-biased ranking;
- relaxed quality thresholds.

Risks:

- lower buyer conversion;
- lower trust;
- higher refunds;
- lower repeat purchase;
- lower match quality.

### 9.3 Platform-Side Wins That May Harm Both Sides

Examples:

- higher take rate;
- higher ad load;
- aggressive monetization;
- reduced support cost by shifting burden to users;
- subsidy reduction without liquidity protection.

Risks:

- lower buyer retention;
- lower seller retention;
- lower transaction quality;
- marketplace trust deterioration.

Agent Action:

- Identify who benefits and who pays.
- Do not call a marketplace intervention successful unless the tradeoff is explicit and acceptable.

---

## 10. Local Market and Segment Scan

The Agent should not rely only on aggregate metrics.

Required segment scans:

- geography;
- category;
- time-of-day;
- day-of-week;
- price band;
- buyer cohort;
- seller cohort;
- new vs existing users;
- high-value vs low-value users;
- dense vs sparse markets;
- high-quality vs low-quality supply;
- new sellers vs mature sellers;
- long-tail sellers vs top sellers.

Segment interpretation rules:

- Do not overreact to noisy small segments.
- Prioritize segments that are strategically important or large enough to affect marketplace health.
- If a harmed segment is core to marketplace supply or trust, treat harm as material even if the aggregate effect is positive.
- If benefits are local-market-specific, recommend `partial_rollout`.

---

## 11. Concentration, Fairness, and Ecosystem Risk

Marketplace algorithms often create concentration.

Short-term conversion may improve by sending more demand to already strong sellers, but long-term supply diversity may weaken.

Agent must check:

- top 1% seller GMV share;
- top 10% seller GMV share;
- exposure Gini;
- earnings Gini;
- search result diversity;
- listing diversity;
- category diversity;
- new seller success;
- long-tail sell-through;
- seller churn by exposure decile;
- buyer choice set diversity.

Decision rule:

- If concentration rises and long-tail seller success falls, do not treat GMV growth as fully healthy.
- If exposure becomes more concentrated but match quality improves, require explicit tradeoff analysis and monitoring.
- If new seller activation or first-sale rate declines, investigate whether the marketplace is reducing future supply formation.

---

## 12. Interference and Network Effects

Marketplace experiments often violate the assumption that one unit's treatment does not affect another unit's outcome.

Interference can occur when treatment changes:

- buyer consideration sets;
- seller visibility;
- prices;
- ranking;
- inventory allocation;
- supply incentives;
- dispatch;
- auctions;
- demand concentration;
- local market competition.

Examples:

- A pricing tool changes seller prices, which changes buyer demand allocation across nearby listings.
- A ranking model sends more traffic to treated sellers and less to control sellers.
- A subsidy increases demand for treated buyers, crowding out untreated buyers in scarce-supply markets.
- A promoted listing product increases seller revenue for advertisers but reduces organic exposure for non-advertisers.
- A dispatch algorithm reduces wait time for some riders by increasing wait time for others.

Agent Action:

- If treatment changes shared resources, do not rely only on individual-level A/B analysis.
- Recommend marketplace-level design when interference risk is material.
- Report market-level outcomes, not only treated-unit outcomes.

Possible designs:

- cluster randomization;
- geo-level experiment;
- market-level holdout;
- switchback experiment;
- time-window randomization;
- synthetic control;
- difference-in-differences;
- matched market design.

### 12.1 Crowding-out and Shadow Demand
In supply-constrained marketplaces, improving conversion for one segment may create "shadow demand" or direct displacement of other high-value users.

* **Audit**: Check if the increase in treated transactions is fully offset by a decrease in untreated/organic transactions within the same supply pool.
* **Rule**: If net marketplace transactions are flat while treated-unit transactions rise, the intervention is merely redistributing supply rather than creating new value.

---

## 13. Marketplace Experiment Design Rules

The Agent must match experiment design to marketplace intervention.

| Intervention Type | Common Randomization Unit | Key Risk | Better Design When Risk Is High |
|---|---|---|---|
| Buyer search ranking | user, session, market | seller exposure spillover | cluster or market-level experiment |
| Seller pricing tool | seller, listing, cluster | nearby supply substitution | listing cluster randomization |
| Subsidy or incentive | buyer, seller, market | crowding out, artificial demand | geo or market-level holdout |
| Dispatch/matching algorithm | market, time window | shared supply pool interference | switchback or market-time design |
| Marketplace fee change | seller, category, market | seller churn and supply response | staged market rollout or DiD |
| Trust/safety policy | seller, listing, market | spillover and policy selection | policy cohort DiD or market holdout |
| Promoted listing / ads | seller, listing, auction | auction displacement | auction-level or market-level design |
| Supply acquisition campaign | geography, cohort | local-market density effects | matched-market or geo experiment |

---

## 14. Scenario Playbooks

### 14.1 GMV Increased

Agent must ask:

- Did completed transactions increase, or only transaction value?
- Did contribution margin improve?
- Did subsidy or incentive cost increase?
- Did refund, cancellation, fraud, or support cost rise?
- Did seller earnings improve or worsen?
- Did growth concentrate among a few sellers or markets?
- Did repeat behavior improve?

Possible decision:

- `healthy_growth` if GMV growth is profitable, high-quality, and balanced.
- `investigate_further` if GMV grows but margin, quality, or seller health is unclear.
- `do_not_launch` if GMV growth is subsidy-driven or low-quality.

### 14.2 Buyer Conversion Increased but Seller Retention Fell

Agent must ask:

- Is seller harm concentrated among strategic sellers?
- Did seller earnings decline?
- Did exposure become more concentrated?
- Did seller response burden increase?
- Are sellers leaving because the intervention worsened economics or fairness?

Likely decision:

- `investigate_further` or `partial_rollout`.
- `do_not_launch` if seller retention or earnings decline is material.

### 14.3 Search-to-Fill Improved but Complaints Increased

Agent must ask:

- Are matches lower quality?
- Did the ranking favor availability over relevance?
- Did cancellations, refunds, or low ratings increase?
- Are users being pushed into poor substitutes?

Likely decision:

- `investigate_further` or `do_not_launch`.

### 14.4 Subsidy Increased Transactions

Agent must ask:

- How many incremental transactions occurred per subsidy dollar?
- Did users retain after subsidy removal?
- Did sellers retain?
- Did subsidy cannibalize organic transactions?
- Did contribution margin deteriorate?
- Did local market density improve durably?

Likely decision:

- `investigate_further` unless incremental durable value is clear.

### 14.5 Ranking Model Improved Conversion but Increased Concentration

Agent must ask:

- Which sellers gained and lost exposure?
- Did top-seller share increase?
- Did long-tail seller first-sale rate fall?
- Did supply diversity decline?
- Did buyer satisfaction improve enough to justify concentration?

Likely decision:

- `launch_with_monitoring` only if concentration remains within tolerance.
- `partial_rollout` or `investigate_further` if long-tail health is uncertain.
- `do_not_launch` if concentration damages supply formation.

### 14.6 Supply Tool Improved Seller Earnings but Buyer Conversion Fell

Agent must ask:

- Did prices increase?
- Did inventory availability improve?
- Did buyer trust or affordability decline?
- Did seller retention improve enough to justify lower conversion?
- Is the tradeoff temporary or structural?

Likely decision:

- `investigate_further` or segment-specific rollout.

### 14.7 Trust/Safety Enforcement Reduced GMV

Agent must ask:

- Did fraud, scams, disputes, or policy violations decline?
- Did buyer trust improve?
- Did seller quality improve?
- Is lost GMV low-quality or harmful?
- Did legitimate sellers suffer false positives?

Likely decision:

- Do not call the intervention bad only because GMV decreased.
- Evaluate quality-adjusted marketplace value.

---

## 15. Marketplace Guardrail Framework

Marketplace guardrails should protect all sides.

### 15.1 Buyer Guardrails

Examples:

- wait time;
- price paid;
- failed search;
- cancellation;
- refund;
- return;
- complaint;
- dispute;
- low rating;
- support ticket;
- trust/safety incident;
- buyer retention.

### 15.2 Seller Guardrails

Examples:

- seller earnings;
- exposure;
- utilization;
- listing conversion;
- response burden;
- seller cancellation;
- seller retention;
- seller churn;
- first sale time;
- long-tail seller success;
- seller satisfaction.

### 15.3 Platform Guardrails

Examples:

- contribution margin;
- support cost;
- fraud cost;
- chargeback;
- policy violation;
- concentration;
- marketplace liquidity;
- operational load;
- brand risk.

* **Operational Overhead**: Ratio of support tickets/appeals to completed transactions;
* **Involuntary Churn**: Rate of accounts blocked or restricted due to policy changes (false positive cost).

### 15.4 Ecosystem Guardrails

Examples:

- category diversity;
- supply diversity;
- exposure fairness;
- new seller formation;
- local-market coverage;
- trust and safety;
- long-term retention on both sides.

---

## 16. Non-Inferiority and Tolerance Logic

Some marketplace guardrails do not need to improve, but they must not deteriorate beyond tolerance.

Examples:

- seller earnings must not decline by more than 0.5%;
- refund rate must not increase by more than 0.2 percentage points;
- cancellation rate must not increase by more than 0.3 percentage points;
- contribution margin must not decline unless justified by durable retention lift;
- top-seller exposure share must not exceed a pre-defined concentration threshold;
- sparse-market fill rate must not decline beyond tolerance;
- buyer complaint rate must not increase beyond tolerance.

Agent Action:

- If guardrail deterioration is within tolerance and the change is reversible, consider `launch_with_monitoring`.
- If guardrail deterioration exceeds tolerance, prefer `do_not_launch` or `investigate_further`.
- For high-risk marketplace changes, require stricter tolerance and longer monitoring.

---

## 17. Decision Matrix

| Evidence Pattern | Recommended Decision |
|---|---|
| OEC improves, liquidity improves, match quality stable, buyer/seller health stable, economics stable | `healthy_growth` |
| OEC improves, guardrails within tolerance, local-market risk remains | `launch_with_monitoring` |
| Benefit concentrated in dense markets or specific categories | `partial_rollout` |
| GMV increases but contribution margin falls due to subsidy | `investigate_further` or `do_not_launch` |
| Buyer conversion improves but seller earnings or retention worsens materially | `investigate_further` or `do_not_launch` |
| Search-to-fill improves but refunds, complaints, or cancellations rise | `investigate_further` or `do_not_launch` |
| Aggregate result positive but sparse markets harmed | `partial_rollout` |
| Top sellers gain share while long-tail seller success declines | `investigate_further` or `do_not_launch` |
| Treatment affects shared inventory, ranking, pricing, or exposure | `use_marketplace_level_experiment` |
| Individual-level experiment likely biased by interference | `use_marketplace_level_experiment` |
| SRM, logging, exposure, or assignment issue affects marketplace metrics | `do_not_trust_result` |
| Trust/safety improves while low-quality GMV falls | Do not treat GMV decline as failure; evaluate quality-adjusted value |
| Short-term transactions rise but buyer or seller retention worsens | `investigate_further` or `do_not_launch` |

---

## 18. Minimum Evidence Required for Marketplace Analysis

A marketplace analysis should include:

### 18.1 Marketplace Context

- marketplace type;
- sides of the marketplace;
- transaction unit;
- matching mechanism;
- intervention;
- decision being made.

### 18.2 Metric Hierarchy

- OEC;
- liquidity metrics;
- match quality metrics;
- buyer health metrics;
- seller health metrics;
- platform economics;
- trust/safety metrics;
- ecosystem metrics.

### 18.3 Supply-Demand Diagnosis

- demand-side liquidity;
- supply-side liquidity;
- market density;
- no-match or no-availability rate;
- utilization;
- local market scan.

### 18.4 Quality and Economics

- completion quality;
- refunds;
- cancellations;
- complaints;
- ratings;
- contribution margin;
- incentive cost;
- support cost;
- fraud or chargeback cost.

### 18.5 Segment and Local Market Effects

- geography;
- category;
- price band;
- time;
- buyer cohort;
- seller cohort;
- supply quality;
- market maturity.

### 18.6 Interference Assessment

- randomization unit;
- shared resource;
- spillover risk;
- market-level outcomes;
- experiment design suitability.

### 18.7 Recommendation

- decision label;
- evidence summary;
- risks;
- missing evidence;
- next analysis;
- rollout and monitoring plan.

---

## 19. Response Template for the Agent

Use this structure when answering a marketplace metrics or marketplace launch question.

```text
Decision: [healthy_growth / launch_with_monitoring / partial_rollout / investigate_further / do_not_launch / use_marketplace_level_experiment / do_not_trust_result]

Marketplace type:
[instant matching / inventory booking / listing commerce / labor/services / creator/content / ads marketplace]

Decision problem:
[Restate the marketplace decision.]

Metric hierarchy:
- OEC / decision metric:
- Liquidity metrics:
- Match quality metrics:
- Buyer health metrics:
- Seller health metrics:
- Platform economics:
- Trust/safety metrics:
- Ecosystem balance metrics:
- Diagnostic metrics:

Supply-demand diagnosis:
[Demand-side and supply-side liquidity readout.]

Quality and economics:
[Match quality, margin, subsidy, support/fraud cost.]

Segment and local-market scan:
[Geography/category/price/time/cohort scan.]

Concentration and ecosystem risk:
[Exposure concentration, long-tail health, supply diversity.]

Interference risk:
[low / medium / high]
[Explain whether ordinary A/B testing is valid.]

Reliable interpretation:
[What can and cannot be concluded.]

Missing evidence:
- [Evidence 1]
- [Evidence 2]
- [Evidence 3]

Next steps:
- [Analysis or experiment design]
- [Rollout/monitoring plan]
- [Rollback threshold]
```

---

## 20. Evaluation Criteria for Agent Answers

A high-quality Agent answer should:

- identify the marketplace type;
- define a durable marketplace OEC;
- avoid treating GMV as sufficient;
- separate liquidity, match quality, buyer health, seller health, economics, and ecosystem balance;
- check both demand-side and supply-side effects;
- scan local markets and segments;
- consider concentration and long-tail supply health;
- evaluate trust, safety, fraud, refunds, and support burden;
- distinguish scale growth from profitable growth;
- identify interference and network effects;
- recommend marketplace-level experimental design when needed;
- choose exactly one decision label;
- state missing evidence and next steps.

Penalize an answer if it:

- says GMV increased, therefore launch;
- ignores seller health when buyer metrics improve;
- ignores buyer experience when seller metrics improve;
- ignores contribution margin and subsidy cost;
- ignores local-market heterogeneity;
- ignores concentration and long-tail supply;
- ignores refunds, cancellations, complaints, or fraud;
- uses ordinary user-level A/B conclusions when interference is likely;
- gives generic marketplace advice without a decision label;
- recommends partial rollout without specifying target market, duration, monitoring, and expansion criteria.

---

## 21. Common Failure Modes

The Agent should avoid these failure modes:

1. **GMV absolutism**

   Treating GMV as the final measure of marketplace health.

2. **Single-sided optimization**

   Optimizing buyer conversion while ignoring seller health, or vice versa.

3. **Ignoring match quality**

   Counting more transactions without checking cancellations, refunds, complaints, or repeat behavior.

4. **Ignoring unit economics**

   Treating subsidy-driven or margin-negative growth as healthy growth.

5. **Aggregate-only reasoning**

   Missing local-market, category, price-band, or cohort harm.

6. **Ignoring concentration**

   Failing to detect that ranking changes help top sellers while weakening long-tail supply.

7. **Ignoring interference**

   Trusting individual-level A/B results when treatment affects shared inventory, pricing, ranking, or exposure.

8. **Confusing liquidity with demand**

   Mistaking more traffic for better matching.

9. **Ignoring supply formation**

   Improving short-term buyer conversion while making it harder for new sellers to succeed.

10. **Overusing partial rollout**

   Recommending partial rollout without specifying where, why, and how expansion will be decided.

---

## 22. Final Rule

The Agent should optimize for durable marketplace health, not surface growth.

A marketplace change is successful only if it improves the ability of demand and supply to find high-quality matches while preserving trust, unit economics, retention, and ecosystem balance.

If the Agent cannot answer who benefits, who is harmed, whether the match quality improved, whether the growth is economically sustainable, and whether interference biases the estimate, it should not recommend broad launch.

The best marketplace answer should feel like a senior marketplace data scientist reviewing a launch decision, not like a dashboard summarizing GMV.

---

## External Methodology References

These references are included to help future maintainers understand the methodological background behind this playbook.

- Airbnb / Holtz et al., "Reducing Interference Bias in Online Marketplace Experiments Using Cluster Randomization: Evidence from a Pricing Meta-Experiment on Airbnb."
- Uber Engineering, "Reinforcement Learning for Modeling Marketplace Balance."
- Uber Engineering, "Improving Gairos Scalability/Reliability."
- Uber Engineering, "Demand and ETR Forecasting at Airports."
- a16z, "13 Metrics for Marketplace Companies."
- Sharetribe Academy, "How to measure marketplace success: the key marketplace metrics."
- Reforge, "Matching Strategies to Improve Marketplace Efficiency."
- Lenny's Newsletter, "The Most Important Marketplace Metrics."
