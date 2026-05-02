# Difference-in-Differences Policy Analysis Playbook

This playbook defines how an agent should evaluate policy, marketplace, product, pricing, operational, or governance changes when clean randomized A/B evidence is unavailable and a quasi-experimental Difference-in-Differences (DiD) design may be appropriate.

The goal is not to teach the agent to run a regression mechanically. The goal is to make the agent behave like a senior causal inference analyst: define the causal question, identify the counterfactual, stress-test the assumptions, choose the correct estimator, expose uncertainty, and decide whether the evidence is strong enough to support a policy or business decision.

A high-quality DiD answer should make clear:

- what treatment or policy is being evaluated;
- which units are treated, untreated, never-treated, or not-yet-treated;
- when treatment starts;
- what outcome is being measured;
- what counterfactual is being assumed;
- whether the parallel trends assumption is plausible;
- whether treatment timing is single, staggered, repeated, or continuous;
- whether selection bias, anticipation, spillover, or concurrent policies threaten identification;
- which estimator is appropriate;
- what robustness checks support or weaken the claim;
- and what causal conclusion, if any, is justified.

The agent should not treat a DiD coefficient as a causal answer until the design survives identification checks.

---

## Quick Retrieval Summary

Use this playbook when the user asks about causal impact from non-randomized policy or rollout evidence.

This playbook is especially relevant when:

- a policy is rolled out to some geographies, markets, stores, schools, creators, sellers, users, or business units but not others;
- the treatment starts at a known date;
- there are pre-treatment and post-treatment observations;
- randomization is unavailable, unethical, or already missed;
- the user asks whether a policy, rule, pricing change, eligibility rule, ranking change, incentive, subsidy, regulation, enforcement policy, or operational intervention caused a change;
- the data is observational but panel-like;
- the treatment was adopted at different times by different groups;
- the user wants to compare treated and untreated trends;
- the user is interpreting a before/after result causally;
- an A/B test is impossible because of policy, network, marketplace, legal, or rollout constraints;
- the user asks for a method such as DiD, event study, PSM-DiD, synthetic control, staggered DiD, or quasi-experiment.

Default reasoning order:

1. Clarify the causal question.
2. Define treatment, unit, time, outcome, and target estimand.
3. Determine whether DiD is appropriate.
4. Audit treatment assignment and selection mechanism.
5. Check data structure and panel integrity.
6. Test and reason about parallel trends.
7. Identify treatment timing structure.
8. Choose the estimator.
9. Check anticipation, spillovers, and concurrent shocks.
10. Run adversarial robustness checks.
11. Interpret magnitude, uncertainty, and heterogeneity.
12. State whether the causal claim is credible.
13. Recommend next action.

---

## 1. Core Principle

Difference-in-Differences is a counterfactual design, not just a subtraction formula.

The central question is:

> Would the treated units have followed the same outcome trend as the control units if the treatment had not occurred?

This is the parallel trends assumption. It is never directly observable after treatment starts. Therefore, the agent must build a credibility argument from design logic, pre-treatment evidence, robustness checks, and domain knowledge.

A good DiD analysis should combine:

- statistical diagnostics;
- institutional knowledge about policy assignment;
- credible comparison group construction;
- modern estimators when treatment timing is staggered;
- sensitivity analysis when assumptions may be imperfect;
- and transparent limits on causal interpretation.

The agent should avoid both extremes:

- overclaiming causality from any treated-control before/after difference;
- rejecting every DiD design because parallel trends cannot be proven.

The correct behavior is to evaluate whether the identifying assumptions are plausible enough for the decision at stake.

---

## 2. Historical and Practical Context

### 2.1 Classical Policy Evaluation

DiD became widely used because many policy changes create natural comparison groups.

A canonical example is the minimum-wage study comparing fast-food restaurants in New Jersey and Pennsylvania before and after New Jersey raised its minimum wage. The treated group was New Jersey restaurants; the comparison group was nearby Pennsylvania restaurants; the estimand was the employment effect of the wage increase.

The historical lesson for the agent:

- DiD is powerful when a policy shock affects one group and not a comparable group.
- The design is only credible if the control group provides a reasonable counterfactual.
- The result must be interpreted in the policy context, not as a generic before/after difference.

### 2.2 Modern Product and Platform Use Cases

In product analytics, DiD is useful when randomized experiments are unavailable.

Examples:

- a feature is launched first in selected cities;
- a pricing rule changes in one market but not another;
- a marketplace policy affects some sellers but not others;
- a recommendation policy changes for eligible creators;
- a fraud rule is activated in high-risk regions;
- a support workflow is introduced in certain queues;
- a compliance requirement applies only to one jurisdiction;
- a platform gradually rolls out a rule across countries.

The agent should treat these as policy evaluations, not standard A/B tests.

### 2.3 Why Modern DiD Needs More Than TWFE

Many real rollouts are staggered: different groups adopt treatment at different times.

Traditional two-way fixed effects (TWFE) can be biased under staggered adoption when treatment effects vary across cohorts or over time. Modern practice often requires group-time average treatment effects, event-study estimators robust to heterogeneity, or decomposition diagnostics.

The agent should not blindly run:

```text
outcome ~ treated * post + unit_fixed_effects + time_fixed_effects
```

unless the design is simple enough and the assumptions are clear.

---

## 3. When DiD Is Appropriate

DiD may be appropriate when:

- treatment affects some units and not others;
- there is at least one pre-treatment period and one post-treatment period;
- treated and control units are observed over time;
- untreated potential outcome trends are plausibly comparable;
- treatment timing is known;
- the outcome is measured consistently over time;
- there are no major concurrent shocks that differentially affect treated units;
- spillovers from treated units to control units are limited or explicitly modeled;
- treatment is not fully determined by an unobserved trend in the outcome.

DiD is stronger when:

- policy assignment is plausibly exogenous;
- treated and control units are similar before treatment;
- pre-treatment trends are visually and statistically similar;
- multiple pre-treatment periods are available;
- there are credible placebo tests;
- estimates are robust to alternative comparison groups and windows;
- the mechanism aligns with the observed timing of the effect.

---

## 4. When Not to Use Simple DiD

Do not use simple DiD when:

- there is no credible comparison group;
- there is only one pre-treatment point and no historical trend evidence;
- treated units were selected because their outcome was already trending differently;
- treatment starts in response to the outcome;
- the control group is contaminated by spillovers;
- another policy changes at the same time only for the treated group;
- treatment timing is staggered but the agent only uses naive TWFE;
- treatment intensity is continuous and binary treatment loses the causal question;
- the outcome definition or logging changed at treatment time;
- treated and control units experience different measurement changes;
- anticipation effects begin before the nominal treatment date;
- units enter or exit the sample because of treatment.

Use a different design when:

- one treated unit and many controls: consider synthetic control or augmented synthetic control.
- policy cutoff determines eligibility: consider regression discontinuity.
- rollout is time-based without a control group: consider interrupted time series, but avoid causal overclaiming.
- treatment assignment is driven by an instrument: consider IV or encouragement designs.
- treatment is randomized by cluster or time: consider cluster RCT or switchback design.
- spillovers are central: use network, cluster, geographic, or exposure-mapping designs.

### 4.1 Design Routing Rules

The agent should not automatically choose DiD whenever the user asks a causal question with observational data.

Before recommending DiD, the agent should route the problem to the most appropriate causal design.

Use a randomized A/B test when:

- treatment can still be randomized;
- interference is limited or can be controlled by cluster randomization;
- the decision can wait for experimental evidence;
- randomization is ethical and operationally feasible.

Use DiD when:

- treated and untreated units both exist;
- treatment starts at a known time;
- pre-treatment and post-treatment data are available;
- the control group can plausibly represent the untreated trend of treated units;
- the treatment is not assigned because the outcome was already changing.

Use staggered DiD when:

- different units adopt treatment at different times;
- treatment effects may vary by cohort or exposure duration;
- not-yet-treated or never-treated units can serve as valid controls.

Use synthetic control when:

- there is one treated unit or very few treated units;
- a donor pool exists;
- pre-treatment fit can be evaluated;
- standard treated-control DiD would depend too heavily on unverifiable comparability.

Use regression discontinuity when:

- treatment assignment depends on a cutoff or threshold;
- units near the cutoff are comparable;
- manipulation around the threshold is limited.

Use interrupted time series only when:

- no credible control group exists;
- the analysis is primarily descriptive or weakly causal;
- pre-treatment time-series patterns are long enough to model;
- the agent clearly warns that causal claims are weaker than in DiD or randomized designs.

Use instrumental variables or encouragement designs when:

- treatment uptake is endogenous;
- there is a credible source of exogenous variation in treatment exposure;
- the exclusion restriction and monotonicity assumptions can be defended.

Routing rule:

- If clean randomization is still possible, prefer experiment design over retrospective DiD.
- If treatment timing is staggered, do not use simple two-period DiD as the primary method.
- If there is only one treated unit, prefer synthetic control or augmented synthetic control.
- If the policy is assigned by a cutoff, consider RD before DiD.
- If no control group exists, use interrupted time series only with limited causal language.

---

## 5. Allowed Causal Status Labels

The agent should use one primary causal status label.

Allowed labels:

- `credible_did`
- `credible_with_caveats`
- `investigate_identification`
- `use_staggered_did`
- `use_weighted_or_matched_did`
- `use_synthetic_control_or_alternative`
- `do_not_trust_causal_claim`
- `descriptive_only`

### 5.1 `credible_did`

Use when the DiD design is strong enough to support a causal interpretation.

Requirements:

- clear treatment date;
- credible comparison group;
- multiple pre-treatment periods;
- parallel trends evidence is supportive;
- no major selection, anticipation, spillover, or concurrent-policy threat;
- estimator matches timing structure;
- inference is clustered correctly;
- robustness checks support the main result.

### 5.2 `credible_with_caveats`

Use when the causal claim is plausible but uncertainty or minor threats remain.

Appropriate when:

- pre-trends are mostly aligned but not perfect;
- one robustness check weakens but does not overturn the result;
- treatment assignment is not random but the selection story is defensible;
- sensitivity analysis shows the result is robust to moderate violations;
- the decision is low-risk or reversible.

The agent must state the caveats explicitly.

### 5.3 `investigate_identification`

Use when the design may be valid, but key identification evidence is missing.

Appropriate when:

- no event study is provided;
- comparison group construction is unclear;
- treatment assignment mechanism is unknown;
- pre-treatment balance is missing;
- treatment timing is ambiguous;
- possible concurrent policies exist;
- the user provides only a coefficient and p-value.

Do not ask only for “more data.” Specify the exact missing diagnostic.

### 5.4 `use_staggered_did`

Use when treatment adoption varies across units over time.

Appropriate methods include:

- Callaway & Sant'Anna group-time ATT;
- Sun & Abraham interaction-weighted event study;
- de Chaisemartin & D'Haultfoeuille style estimators;
- Borusyak-Jaravel-Spiess imputation;
- Gardner two-stage DiD;
- Bacon decomposition as a diagnostic.

Avoid naive TWFE as the primary estimator unless treatment effects are plausibly homogeneous and decomposition checks are clean.

### 5.5 `use_weighted_or_matched_did`

Use when treated and control units differ strongly on pre-treatment covariates or pre-treatment outcomes, but overlap exists.

Possible approaches:

- propensity score weighting;
- propensity score matching plus DiD;
- entropy balancing on covariates and pre-treatment outcomes;
- inverse probability weighting;
- doubly robust DiD.

The agent must emphasize that matching and weighting address observed imbalance only. They do not fix unobserved differential trends automatically.

### 5.6 `use_synthetic_control_or_alternative`

Use when a DiD comparison group is weak or there are too few treated units.

Examples:

- one state adopts a policy;
- one city changes enforcement;
- one country introduces a rule;
- one product region receives a policy;
- comparison units do not share pre-treatment trends.

Consider synthetic control, augmented synthetic control, matrix completion, regression discontinuity, interrupted time series, IV, or a future randomized rollout.

### 5.7 `do_not_trust_causal_claim`

Use when the design is broken enough that the causal conclusion should not be used.

Examples:

- treatment is assigned because of a pre-existing trend in the outcome;
- pre-treatment trends clearly diverge and no credible adjustment exists;
- control units are heavily contaminated;
- a simultaneous shock affects only treated units;
- outcome measurement changes at the policy date;
- post-treatment sample filtering creates collider bias;
- the treatment date is chosen after looking at the outcome;
- the result depends entirely on one outlier or one arbitrary window.

### 5.8 `descriptive_only`

Use when the analysis can describe changes but cannot support causal claims.

Examples:

- before/after comparison with no control;
- cross-sectional treated-control comparison with no time dimension;
- incomplete treatment timing;
- insufficient pre-periods;
- no plausible counterfactual.

---

## 6. Core DiD Notation

The agent should map each problem into a structured design.

Required fields:

```text
Unit:
Time period:
Treatment:
Treatment start:
Outcome:
Treated group:
Control group:
Never-treated units:
Not-yet-treated units:
Target estimand:
Treatment timing:
Main estimator:
Inference level:
Validity threats:
```

Canonical 2x2 DiD estimand:

```text
ATT = [E(Y_treated,post) - E(Y_treated,pre)]
    - [E(Y_control,post) - E(Y_control,pre)]
```

Panel TWFE form:

```text
Y_it = alpha_i + gamma_t + beta * D_it + epsilon_it
```

Event-study form:

```text
Y_it = alpha_i + gamma_t + Σ_k beta_k * 1[event_time_it = k] + epsilon_it
```

The agent should not present formulas without explaining the causal assumption.

### 6.1 Agent Tool Execution Protocol

This playbook is designed for an agent that can inspect data, run diagnostics, choose an estimator, and produce an auditable causal recommendation.

The agent should execute DiD analysis in a fixed order. It should not estimate the treatment effect before validating the design.

Required input fields:

```text
unit_id
time_id
outcome
treatment_indicator
treatment_start_time
treated_group_indicator
cohort_or_adoption_time
control_group_indicator
covariates
denominator, if the outcome is a rate
sample_inclusion_indicator, if available
geography
platform
market
user_segment
seller_or_creator_segment
baseline_outcome
baseline_trend
policy_announcement_time
implementation_time
exposure_intensity
risk_score
cluster_id

---

## 7. Required Reasoning Order

### Step 1: Clarify the Causal Question

Identify the causal question before choosing a method.

Good causal questions:

- Did the policy reduce churn among affected users?
- Did the marketplace rule increase seller retention?
- Did the pricing change reduce demand?
- Did the enforcement policy reduce harmful behavior?
- Did the launch in treated cities increase conversion relative to comparable cities?

Bad causal questions:

- Did the metric go up after the policy?
- Is the treated group higher than the control group?
- Is the coefficient statistically significant?

The agent should rewrite vague questions into:

```text
What is the average treatment effect on the treated units after policy adoption, relative to a credible counterfactual untreated trend?
```

---

### Step 2: Define Unit, Time, Treatment, and Outcome

A DiD design fails if these are ambiguous.

The agent should define:

- unit: user, seller, creator, store, county, city, market, school, firm, advertiser, product surface;
- time: day, week, month, quarter;
- treatment: policy exposure, eligibility, enforcement, feature availability, price change, rule change;
- outcome: retention, revenue, conversion, employment, complaints, fraud, liquidity, quality;
- treatment date: first exposure date or enforcement date;
- exposure definition: intent-to-treat vs actual treatment-on-treated;
- analysis population: assigned, eligible, active, observed, or exposed units.

Default preference:

- use intent-to-treat when eligibility or policy assignment is the causal intervention;
- avoid conditioning on post-treatment exposure or activity unless the estimand is explicitly treatment-on-treated and identification is addressed.

---

### Step 3: Determine Whether Treatment Assignment Is Plausibly Exogenous

The agent should audit why units were treated.

Treatment assignment can be:

- quasi-random policy shock;
- geography-based legal change;
- operational rollout capacity;
- phased rollout by engineering constraints;
- voluntary adoption;
- performance-based targeting;
- risk-based enforcement;
- business-priority targeting;
- user self-selection.

Assignment credibility ranking:

1. externally imposed policy shock;
2. randomized or capacity-driven rollout unrelated to outcomes;
3. administrative rollout with documented non-outcome reasons;
4. eligibility-rule assignment based on pre-treatment covariates;
5. voluntary adoption;
6. treatment assigned because outcome was already changing.

If treatment is assigned because of the outcome trend, simple DiD is usually not credible.

---

### Step 4: Construct the Counterfactual

The control group should answer:

> What would have happened to the treated units if they had not been treated?

The agent should check:

- Are control units exposed to the same macro shocks?
- Are they similar in pre-treatment levels and trends?
- Are they in the same market, product surface, or institutional environment?
- Are they unaffected by treatment?
- Are they not strategically responding to treated units?
- Do they have enough observations before and after treatment?
- Are they eligible for treatment later, never treated, or structurally different?

Control group options:

- never-treated units;
- not-yet-treated units;
- matched controls;
- weighted controls;
- synthetic controls;
- geographic neighbors;
- same-unit historical controls, only as a weak fallback.

Control group warning:

- Not-yet-treated units can be valid before their own treatment starts.
- Already-treated units are dangerous controls when effects persist.
- Units selected for non-adoption may differ systematically from treated units.

---

### Step 5: Check Data Structure and Integrity

Before estimation, verify:

- unit-time panel completeness;
- duplicate unit-time rows;
- missing outcomes;
- treatment coding consistency;
- exact treatment date;
- exposure window;
- time zone alignment;
- aggregation level;
- denominator changes;
- unit entry and exit;
- outcome definition stability;
- logging or measurement changes;
- policy implementation lag;
- sample composition stability;
- whether treatment changes observation probability.

Panel checks:

```text
- Count units by treatment cohort.
- Count observations per unit.
- Check balanced vs unbalanced panel.
- Check pre/post coverage.
- Check missing outcome by cohort and time.
- Check whether treatment predicts sample inclusion.
```

If treatment changes who is observed, the agent must flag selection into the sample.

---

## 8. Parallel Trends First

Parallel trends is the central identifying assumption.

The agent should treat PTA as a design requirement, not a decorative chart.

### 8.1 What Parallel Trends Means

Parallel trends means that, absent treatment, treated and control units would have experienced the same average outcome trend.

It does not require:

- identical outcome levels;
- identical covariates;
- identical baseline sizes.

It does require:

- comparable untreated trend evolution.

### 8.2 What the Agent Must Check

Minimum checks:

1. plot average outcome by group over time;
2. estimate event-study coefficients;
3. inspect pre-treatment leads;
4. check pre-treatment outcome levels and slopes;
5. test placebo treatment dates before actual treatment;
6. compare alternative control groups;
7. assess whether domain logic supports shared shocks;
8. evaluate sensitivity to plausible trend deviations.

### 8.3 Event Study Requirements

The event study should show:

- pre-treatment coefficients;
- treatment-period coefficient omitted as baseline;
- post-treatment dynamic effects;
- confidence intervals;
- sample sizes by relative time;
- cohort composition by relative time if staggered adoption exists.

Interpretation rules:

- Flat pre-period coefficients support credibility but do not prove parallel trends.
- Significant pre-trends weaken credibility.
- Lack of significant pre-trends is weak evidence when power is low.
- If post-treatment effects appear before treatment, check anticipation, data leakage, or invalid timing.
- If effects grow gradually after treatment, mechanism should explain why.

### 8.4 Do Not Use Pre-Trend Tests Mechanically

Bad reasoning:

> The pre-trend p-value is above 0.05, so parallel trends holds.

Better reasoning:

> The event-study pre-period coefficients are small relative to the post-period effect, visually stable, and robust across alternative control groups. However, power is limited, so the analysis should include sensitivity to moderate PTA violations.

### 8.5 Sensitivity to Parallel-Trend Violations

If PTA is plausible but not guaranteed, use sensitivity analysis.

Options:

- HonestDiD / Rambachan-Roth sensitivity;
- allow group-specific linear trends;
- compare estimates with and without trend adjustment;
- restrict to more comparable controls;
- entropy balance on pre-treatment outcomes;
- placebo outcome tests;
- alternative pre/post windows;
- synthetic control comparison.

The agent should ask:

> How large would a violation of parallel trends need to be to overturn the conclusion?

---

## 9. Selection Bias and Counterfactual Quality

Selection bias is a major threat in policy DiD.

### 9.1 Selection Mechanisms to Audit

The agent should classify selection as:

- random or externally imposed;
- administrative but unrelated to outcome trends;
- based on observable pre-treatment characteristics;
- based on prior outcome levels;
- based on prior outcome trends;
- voluntary;
- strategic;
- risk-triggered;
- capacity-constrained;
- politically selected;
- selected because units were already improving or deteriorating.

Selection into treatment based on pre-treatment outcome trends is especially dangerous.

* **Selection on Gains**: Units adopt treatment specifically because they anticipate a higher-than-average benefit (e.g., power users opting into a beta). This makes the ATT non-representative of the general population.

### 9.2 Matching or Weighting

Use matching or weighting when treated and control units differ on observables but overlap exists.

Options:

- propensity score matching;
- propensity score weighting;
- entropy balancing;
- coarsened exact matching;
- nearest-neighbor matching on pre-treatment outcomes;
- doubly robust DiD;
- covariate-adjusted group-time ATT.

Matching and weighting should be done using pre-treatment variables only.

Never match on post-treatment variables.

### 9.3 Balance Checks

After matching or weighting, report:

- covariate balance;
- pre-treatment outcome balance;
- pre-treatment trend balance;
- effective sample size;
- common support;
- units dropped;
- extreme weights;
- weight concentration;
- sensitivity to trimming.

If balance improves but pre-trends still diverge, causal credibility remains weak.

### 9.4 What Matching Cannot Fix

Matching does not automatically solve:

- unobserved treatment selection;
- differential shocks;
- anticipation;
- spillovers;
- treatment misclassification;
- endogenous policy timing.

The agent should not overstate PSM-DiD as a magic correction.

---

## 10. Treatment Timing Patterns and Estimator Choice

### 10.1 Single Treatment Date, Two Groups

Use canonical DiD when:

- one treated group;
- one comparison group;
- one policy start date;
- stable treatment exposure;
- no staggered adoption.

Possible estimator:

```text
Y_it = alpha_i + gamma_t + beta * Treated_i * Post_t + epsilon_it
```

Still required:

- event-study pre-trend check;
- clustered standard errors;
- placebo tests;
- robustness to windows and controls.

### 10.2 Multiple Treated Cohorts / Staggered Adoption

Use modern staggered DiD methods when:

- different units adopt at different times;
- treatment effects may vary across cohorts;
- treatment effects may evolve over exposure duration;
- already-treated units would appear as controls in naive TWFE.

Preferred estimators:

- Callaway & Sant'Anna group-time ATT;
- Sun & Abraham interaction-weighted event study;
- Borusyak-Jaravel-Spiess imputation estimator;
- de Chaisemartin & D'Haultfoeuille estimators;
- Gardner two-stage DiD.

Diagnostics:

- Bacon decomposition;
- cohort-specific event studies;
- group-time ATT heatmap;
- comparison of never-treated vs not-yet-treated controls;
- sensitivity to excluding early-treated or late-treated cohorts.

Decision rule:

- If naive TWFE differs materially from robust staggered estimators, do not rely on TWFE.
- If the sign changes across estimators, use `investigate_identification` or `do_not_trust_causal_claim`.

### 10.3 Repeated or Reversible Treatments

If treatment can turn on and off:

- simple absorbing-treatment DiD may be wrong;
- define exposure duration and washout;
- consider switchback designs;
- model treatment histories;
- avoid using already affected periods as clean controls;
- check lagged effects and carryover.

### 10.4 Continuous Treatment Intensity

If treatment varies in intensity:

- avoid arbitrary binarization unless justified;
- define dose-response estimand;
- use generalized DiD or continuous treatment methods;
- check whether treatment intensity is endogenous;
- report effects per meaningful unit of intensity.

Examples:

- subsidy amount;
- ad load;
- enforcement probability;
- tax rate;
- discount depth;
- exposure share;
- policy strictness.

### 10.5 One Treated Unit

If only one unit is treated, standard DiD may be fragile.

Consider:

- synthetic control;
- augmented synthetic control;
- matrix completion;
- comparative interrupted time series;
- permutation or placebo-in-space tests.

The agent should not overstate precision from one treated unit.

### 10.6 Repeated Cross-Sections

If the same individual units are not observed over time but comparable samples exist:

- DiD may still be possible;
- define group-time cells;
- ensure outcome measurement is stable;
- account for changing sample composition;
- use survey weights if relevant;
- avoid interpreting individual-level persistence.

### 10.7 Triple Differences (DDD)
Use Triple Differences when you suspect a concurrent shock or a group-specific trend violation that DiD cannot capture.

* **Logic**: Compare the DiD of the target population with the DiD of a "placebo" population within the same treated region that should not be affected by the policy.
* **Example**: A city-wide tax on luxury goods. Compare (Luxury vs. Essentials in Treated City) to (Luxury vs. Essentials in Control City).
* **Requirement**: The third dimension must be immune to the treatment but subject to the same local shocks.

---

## 11. Staggered Adoption and the TWFE Trap

### 11.1 Why Naive TWFE Can Fail

With staggered adoption, TWFE can compare:

- treated units to never-treated units;
- treated units to not-yet-treated units;
- earlier-treated units to later-treated units;
- later-treated units to already-treated units.

The last comparison can be problematic when treatment effects persist or change over time. Already-treated units may no longer represent untreated counterfactuals.

### 11.2 Forbidden Comparison Warning

The agent should flag possible forbidden comparisons when:

- treatment effects are dynamic;
- treatment effects differ across cohorts;
- adoption timing is correlated with treatment effect size;
- no never-treated units exist;
- early adopters and late adopters have different baseline trends;
- TWFE weights are negative or unintuitive.

### 11.3 Required Diagnostics

For staggered designs, the agent should request or compute:

- cohort counts;
- adoption timing distribution;
- never-treated availability;
- group-time ATT estimates;
- event-time effects by cohort;
- Bacon decomposition;
- robust estimator comparison;
- sensitivity to excluding cohorts.

### 11.4 Recommended Output

The agent should report:

```text
Primary estimand:
- ATT(g, t), aggregated by cohort and event time.

Primary estimator:
- [CS-DiD / Sun-Abraham / BJS / two-stage DiD]

Control group:
- [never-treated / not-yet-treated]

TWFE status:
- [not used / used only as diagnostic / acceptable because ...]
```

---

## 12. Anticipation Effects

Anticipation occurs when units change behavior before treatment officially starts because they expect the policy.

Examples:

- users rush to act before a price increase;
- firms adjust employment before regulation starts;
- sellers change inventory before a marketplace rule;
- creators alter content before enforcement;
- advertisers shift budgets before a bidding rule change.

The agent should check:

- announcement date vs implementation date;
- whether treatment was predictable;
- event-study lead effects;
- outcome movement between announcement and implementation;
- pre-policy communication or warnings.

Handling options:

- redefine treatment start at announcement date;
- exclude anticipation window;
- model separate announcement and implementation effects;
- avoid causal claims if anticipation is inseparable.

---

## 13. Spillovers and SUTVA Violations

DiD assumes untreated units are not affected by treated units.

This can fail in:

- marketplaces;
- social networks;
- geographic mobility;
- creator ecosystems;
- seller competition;
- search ranking;
- ad auctions;
- school choice;
- labor markets;
- shared inventory systems;
- fraud enforcement;
- content moderation.

### 13.1 Spillover Types

Common spillovers:

- geographic spillover;
- network spillover;
- demand displacement;
- supply displacement;
- competitive response;
- contamination through shared users;
- treatment-induced migration;
- resource reallocation;
- equilibrium price changes.

### 13.2 How to Diagnose Spillovers

The agent should check:

- whether control units interact with treated units;
- distance to treated units;
- shared marketplace inventory;
- shared users or sellers;
- network links;
- cross-border movement;
- market-level aggregate changes;
- displacement from treated to control areas;
- indirect exposure variables.

### 13.3 Design Responses

Possible responses:

- cluster-level treatment definition;
- geographic buffers;
- exclude neighboring controls;
- exposure mapping;
- market-level aggregation;
- network cluster design;
- switchback design;
- randomized saturation design;
- separate direct and indirect effects.

If spillovers are likely and unmodeled, use `investigate_identification` or `do_not_trust_causal_claim`.

---

## 14. Concurrent Policies and Confounding Shocks

A DiD estimate can be invalid if another shock changes at the same time for treated units.

The agent should audit:

- other product launches;
- policy changes;
- pricing changes;
- enforcement changes;
- marketing campaigns;
- seasonality;
- macro shocks;
- platform outages;
- competitor actions;
- regulatory events;
- measurement changes;
- operational staffing changes;
- supply shocks.

Recommended checks:

- timeline of all relevant events;
- placebo outcomes unaffected by treatment;
- alternative control groups exposed to similar shocks;
- covariate adjustment for known shocks;
- exclusion of contaminated windows;
- triple-difference design if a second comparison dimension exists.

If the concurrent shock cannot be separated from treatment, do not claim a clean DiD effect.

---

## 15. Inference and Standard Errors

### 15.1 Cluster at the Treatment Assignment Level

Default:

- cluster standard errors at the unit level or treatment assignment level.

Examples:

- state-level policy: cluster by state;
- city-level policy: cluster by city;
- store-level policy: cluster by store;
- seller-level policy: cluster by seller;
- school-level policy: cluster by school.

If treatment varies at a higher level than observations, cluster at that higher level.

### 15.2 Serial Correlation

Panel outcomes are often serially correlated. Ignoring serial correlation can produce overconfident p-values.

The agent should avoid naive OLS standard errors.

### 15.3 Few Clusters

If there are few treated or total clusters:

- use wild cluster bootstrap;
- use randomization inference;
- report sensitivity to cluster assumptions;
- avoid overclaiming precise p-values.

### 15.4 Multiple Outcomes and Multiple Testing

When many outcomes or segments are tested:

- classify primary vs secondary outcomes before analysis;
- adjust or clearly label exploratory results;
- control false discovery when appropriate;
- avoid cherry-picking the most favorable metric.

---

## 16. Adversarial Robustness Checks

A top-level DiD agent should behave like an auditor.

### 16.1 Placebo Treatment Date

Move the treatment date to a pre-treatment period.

Expected result:

- no effect before actual treatment.

If the placebo treatment shows an effect, the design may be capturing pre-existing trend differences.

### 16.2 Placebo Treated Group

Assign treatment to units that were never treated.

Expected result:

- no systematic effect.

If many placebo groups show similar effects, the result may reflect common shocks or model artifacts.

### 16.3 Placebo Outcome

Use outcomes that should not be affected by treatment.

Examples:

- pre-policy outcome;
- unrelated product metric;
- unaffected demographic behavior;
- invariant administrative measure.

If placebo outcomes move, the design may be confounded.

### 16.4 Alternative Control Groups

Re-estimate using:

- geographic neighbors;
- matched controls;
- never-treated controls;
- not-yet-treated controls;
- synthetic controls;
- restricted controls with similar pre-trends.

If results depend entirely on one control group, credibility weakens.

### 16.5 Window Sensitivity

Vary:

- pre-period length;
- post-period length;
- excluded anticipation window;
- treatment ramp-up period;
- seasonality controls.

A real policy effect should not depend on an arbitrary window unless the mechanism justifies it.

### 16.6 Cohort Sensitivity

For staggered rollouts:

- drop early adopters;
- drop late adopters;
- estimate cohort-specific effects;
- compare high-risk and low-risk cohorts;
- test whether adoption timing predicts effect size.

### 16.7 Outlier and Influence Analysis

Check:

- whether one unit drives the result;
- winsorization sensitivity;
- leave-one-cluster-out estimates;
- abnormal outcome spikes;
- data entry or logging anomalies;
- policy exceptions.

### 16.8 Functional Form Robustness

Compare:

- levels vs logs;
- rates vs counts with denominators;
- weighted vs unweighted estimates;
- Poisson or binomial models for count/rate outcomes;
- alternative denominator definitions.

### 16.9 Instrumentation and Logging Parity
Verify that the way the outcome is measured did not change differentially at the time of treatment.

* **Audit**: Check if the "Treatment Group" received a new logging version or UI component that captures events more (or less) accurately than the "Control Group".
* **Rule**: If the policy launch coincided with a telemetry upgrade only for treated units, the result is likely an artifact of instrumentation.

---

## 17. Heterogeneous Treatment Effects

The average effect may hide important variation.

The agent should check heterogeneity by:

- treatment cohort;
- event time since treatment;
- geography;
- market maturity;
- baseline outcome level;
- baseline trend;
- user type;
- seller or creator segment;
- advertiser size;
- product surface;
- platform;
- risk tier;
- policy intensity;
- compliance status.

Interpretation rules:

- Pre-specify key segments when possible.
- Treat exploratory segment findings cautiously.
- Report uncertainty by segment.
- Avoid launching or recommending policy expansion if a strategic segment is harmed.
- Do not average away meaningful harm to protected, high-value, or policy-sensitive groups.

---

## 18. Practical Magnitude and Decision Relevance

Statistical significance is not enough.

The agent should report:

- absolute effect;
- relative effect;
- baseline level;
- confidence interval;
- business impact;
- cost-benefit interpretation;
- harmed and benefited segments;
- timing of effect;
- persistence;
- uncertainty under robustness checks.

A small statistically significant effect may not justify policy complexity.

A large but fragile estimate may not support a high-stakes decision.

A non-significant result may still be important if the confidence interval includes meaningful harm or benefit.

---

## 19. Scenario Playbooks

### 19.1 State or City Policy Change

Examples:

- minimum wage;
- tax change;
- privacy regulation;
- public health policy;
- transit policy;
- housing policy.

Recommended design:

- DiD with comparable geographies;
- event study;
- clustered standard errors by geography;
- robustness to neighboring controls;
- check migration and spillovers;
- check concurrent regional policies;
- consider synthetic control if one treated geography.

### 19.2 Product Policy Rollout by Geography

Examples:

- feature available in selected cities;
- delivery fee policy in selected markets;
- new marketplace rule in selected countries.

Recommended design:

- staggered DiD if rollout timing varies;
- market-level panel;
- control for seasonality;
- check rollout assignment reason;
- test spillovers across markets;
- monitor marketplace displacement.

### 19.3 Eligibility Rule or Threshold Policy

Examples:

- sellers above a risk score receive enforcement;
- users above eligibility threshold receive subsidy;
- advertisers above spend threshold enter a new rule.

Recommended design:

- regression discontinuity if threshold is sharp;
- DiD around threshold if policy also changes over time;
- avoid comparing high-risk and low-risk units without adjustment;
- check manipulation around threshold.

### 19.4 Voluntary Adoption

Examples:

- firms choose to adopt a tool;
- users opt into a new feature;
- sellers choose a program.

Recommended design:

- DiD only with strong selection correction;
- match or weight on pre-treatment behavior;
- event study around adoption;
- check whether adoption follows outcome trends;
- consider IV or encouragement design if available.

Default status:

- usually `investigate_identification` or `use_weighted_or_matched_did`.

### 19.5 Enforcement or Risk-Based Policy

Examples:

- fraud detection rule;
- content moderation enforcement;
- account restriction policy.

Risk:

- treated units are selected because they are already risky.

Recommended design:

- avoid naive treated-control DiD;
- compare near-threshold units;
- use policy cutoff if available;
- model risk score and pre-trends;
- check displacement and adversarial adaptation;
- distinguish true harm reduction from measurement changes.

### 19.6 Marketplace Intervention

Examples:

- seller ranking rule;
- buyer subsidy;
- creator monetization policy;
- ad auction rule;
- search ranking change.

Risks:

- spillovers;
- displacement;
- equilibrium effects;
- harmed untreated units;
- supply-demand rebalancing.

Recommended design:

- market-level or cluster-level DiD;
- exposure mapping;
- holdout markets;
- switchback if feasible;
- measure both sides of marketplace;
- check total ecosystem value, not only treated-unit outcome.

### 19.7 One Treated Region or One Treated Business Unit

Recommended design:

- synthetic control;
- augmented synthetic control;
- placebo-in-space;
- leave-one-control-out;
- avoid overconfidence from standard DiD.

---

## 20. Minimum Evidence Required for a DiD Memo

A causal memo should include:

### 20.1 Causal Question

- treatment;
- affected units;
- outcome;
- time horizon;
- target estimand;
- decision being supported.

### 20.2 Policy and Assignment Context

- why treatment happened;
- why some units were untreated;
- whether assignment was exogenous;
- whether adoption was staggered;
- announcement and implementation dates;
- concurrent policy timeline.

### 20.3 Data Description

- unit and time granularity;
- panel coverage;
- sample restrictions;
- treatment coding;
- outcome definition;
- missingness;
- denominator;
- pre/post windows.

### 20.4 Identification Strategy

- counterfactual logic;
- parallel trends argument;
- control group construction;
- estimator;
- inference method;
- assumptions.

### 20.5 Diagnostics

- pre-trend plot;
- event-study leads and lags;
- balance table;
- panel integrity checks;
- treatment assignment audit;
- spillover and anticipation checks.

### 20.6 Results

- main effect estimate;
- uncertainty;
- practical magnitude;
- dynamic effects;
- heterogeneous effects;
- business or policy impact.

### 20.7 Robustness

- placebo date;
- placebo group;
- placebo outcome;
- alternative controls;
- alternative windows;
- matching or weighting sensitivity;
- cohort sensitivity;
- outlier influence;
- sensitivity to PTA violations.

### 20.8 Conclusion

- causal status label;
- whether evidence supports a causal claim;
- limitations;
- next steps;
- whether to act, monitor, rerun, redesign, or use another method.

---

## 21. Agent Response Template

When answering a DiD policy-analysis question, use this structure.

```text
Causal status: [credible_did / credible_with_caveats / investigate_identification / use_staggered_did / use_weighted_or_matched_did / use_synthetic_control_or_alternative / do_not_trust_causal_claim / descriptive_only]

Decision problem:
[Restate the causal question and decision.]

Design summary:
- Unit:
- Time period:
- Treatment:
- Treatment start:
- Outcome:
- Treated group:
- Control group:
- Target estimand:
- Treatment timing:

Identification assessment:
1. Assignment mechanism:
2. Counterfactual quality:
3. Parallel trends evidence:
4. Anticipation risk:
5. Spillover/SUTVA risk:
6. Concurrent policy risk:
7. Measurement/data integrity:

Estimator recommendation:
[Canonical DiD / event study / CS-DiD / Sun-Abraham / BJS / synthetic control / PSM-DiD / entropy-balanced DiD / alternative design]

Evidence interpretation:
[Effect size, uncertainty, practical magnitude, heterogeneity.]

Robustness required:
- [Check 1]
- [Check 2]
- [Check 3]

Conclusion:
[What causal claim is justified, if any.]

Next steps:
- [Analysis step]
- [Data/design step]
- [Decision step]
```

---

## 22. Decision Matrix

| Evidence Pattern | Recommended Causal Status |
|---|---|
| Clear policy shock, comparable controls, supportive event study, no major threats, correct inference | `credible_did` |
| Mostly supportive evidence, but minor PTA or design caveats remain | `credible_with_caveats` |
| Coefficient provided but no pre-trend, assignment, or control-group diagnostics | `investigate_identification` |
| Treatment adoption is staggered across cohorts | `use_staggered_did` |
| Treated and controls are observably imbalanced but overlap exists | `use_weighted_or_matched_did` |
| One treated unit or weak controls | `use_synthetic_control_or_alternative` |
| Strong pre-trend divergence with no credible adjustment | `do_not_trust_causal_claim` |
| Treatment selected based on outcome trend | `do_not_trust_causal_claim` |
| Before/after only, no control group | `descriptive_only` |
| Control group likely affected by treatment spillovers | `investigate_identification` or `do_not_trust_causal_claim` |
| Concurrent policy affects only treated units at same time | `investigate_identification` or `do_not_trust_causal_claim` |
| TWFE used under staggered adoption with heterogeneous effects and no diagnostics | `use_staggered_did` |
| Placebo tests show similar effects before treatment | `do_not_trust_causal_claim` |
| Result survives placebo, alternative controls, window, and sensitivity checks | `credible_did` or `credible_with_caveats` |

---

## 23. Evaluation Criteria for Agent Answers

A high-quality answer should:

- state one causal status label;
- define the treatment, unit, time, outcome, and estimand;
- explain whether DiD is appropriate;
- inspect treatment assignment and selection bias;
- prioritize parallel trends before interpreting coefficients;
- require event-study evidence;
- choose an estimator that matches treatment timing;
- warn against naive TWFE under staggered adoption;
- discuss anticipation effects;
- discuss spillovers and SUTVA violations;
- discuss concurrent policies and measurement changes;
- cluster inference correctly;
- distinguish statistical significance from practical magnitude;
- perform or request adversarial robustness checks;
- explain uncertainty and limitations;
- recommend a concrete next step.

Penalize an answer if it:

- treats a DiD coefficient as causal without discussing parallel trends;
- says “p < 0.05, so the policy worked”;
- uses naive TWFE for staggered adoption without diagnostics;
- ignores selection into treatment;
- ignores anticipation or spillovers;
- ignores concurrent policy changes;
- matches on post-treatment variables;
- overstates PSM or entropy balancing as solving all selection problems;
- uses already-treated units as controls without caution;
- reports only the average effect while hiding cohort heterogeneity;
- fails to state the control group;
- fails to describe treatment timing;
- fails to cluster standard errors appropriately;
- gives a confident causal conclusion with only before/after data.

A strong answer should feel like a senior causal inference reviewer auditing the design, not a generic regression summary.

---

## 24. Common Failure Modes

### 24.1 Coefficient Worship

Bad:

> The interaction coefficient is positive and significant, so the policy worked.

Better:

> The coefficient is positive, but causal interpretation depends on parallel trends, assignment credibility, no spillovers, and no concurrent shocks.

### 24.2 Parallel-Trends Checkbox

Bad:

> The pre-trend test is insignificant, so PTA holds.

Better:

> Pre-trends are visually small and economically minor, but power is limited. Sensitivity analysis is needed to determine whether plausible violations would overturn the result.

### 24.3 Naive TWFE Under Staggered Adoption

Bad:

> We included unit and time fixed effects, so the staggered rollout is handled.

Better:

> With staggered adoption and dynamic treatment effects, TWFE may mix clean and contaminated comparisons. Use group-time ATT or interaction-weighted event study.

### 24.4 Bad Control Group

Bad:

> Control units are untreated, so they are valid controls.

Better:

> Untreated status is not enough. Controls must provide a credible untreated trend for treated units.

### 24.5 Matching as Magic

Bad:

> We matched treated and control units, so selection bias is gone.

Better:

> Matching improves observable balance, but the causal claim still requires parallel trends conditional on matched covariates and no unobserved differential shocks.

### 24.6 Ignoring Spillovers

Bad:

> The control group was not directly treated, so it is unaffected.

Better:

> In marketplaces, networks, and geographies, untreated units may be indirectly affected. Spillovers must be tested or modeled.

### 24.7 Post-Treatment Conditioning

Bad:

> We analyze only users who remained active after the policy.

Better:

> Activity after treatment may be affected by treatment. Conditioning on it can introduce bias.

### 24.8 Arbitrary Window Selection

Bad:

> The effect is significant in the chosen 4-week window.

Better:

> The result should be robust to reasonable pre/post windows unless the mechanism predicts that exact timing.

### 24.9 Ignoring Measurement Changes

Bad:

> Reports dropped after enforcement, so harm declined.

Better:

> If reporting UI, logging, or enforcement definitions changed, the measured decline may reflect instrumentation rather than behavior.

### 24.10 Averaging Away Harm

Bad:

> The average effect is positive, so the policy is beneficial.

Better:

> The average effect can hide harm to high-value, protected, vulnerable, or strategically important segments.

---

## 25. Final Rule

The agent should not ask “What is the DiD estimate?” first.

It should ask:

> What counterfactual makes this estimate causal, and how hard have we tried to break that counterfactual?

When the counterfactual is credible, use DiD to support causal decision-making.

When the counterfactual is uncertain, label the result as provisional and run robustness checks.

When the counterfactual is broken, do not present the coefficient as causal.

The best DiD analysis is not the one with the smallest p-value. It is the one where the identifying assumption, estimator, robustness checks, and business interpretation all point to the same conclusion.

---

## 26. Method Anchors and Further Reading

The playbook is grounded in commonly used DiD and quasi-experimental methods, including:

- Card & Krueger: minimum wage natural experiment comparing New Jersey and Pennsylvania fast-food restaurants.
- World Bank DIME: practical DiD guidance and parallel-trends discussion.
- Goodman-Bacon: decomposition of TWFE DiD with variation in treatment timing.
- Callaway & Sant'Anna: group-time average treatment effects for DiD with multiple time periods.
- Sun & Abraham: event-study estimation under heterogeneous treatment effects.
- Rambachan & Roth / HonestDiD: sensitivity analysis for violations of parallel trends.
- Hainmueller: entropy balancing for covariate balance in observational studies.
- Stuart et al.: propensity-score methods combined with DiD in policy and health-services research.

For this agentic RAG project, these references should be treated as method anchors. The agent should retrieve the relevant section of this playbook first, then choose the estimation and diagnostic path that matches the user's scenario.
