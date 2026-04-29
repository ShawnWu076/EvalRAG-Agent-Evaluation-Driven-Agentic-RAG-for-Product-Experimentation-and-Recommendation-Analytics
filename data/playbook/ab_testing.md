# A/B Testing Playbook

## Purpose

A randomized A/B test estimates the causal effect of a product change by assigning eligible users or units to control and treatment before exposure. The assignment mechanism matters as much as the metric movement. If assignment is biased, if exposure logging is incomplete, or if the analysis population changes after randomization, the measured lift may not represent the treatment effect.

## Decision Principles

Start with a clear hypothesis, a primary metric, guardrail metrics, and a launch threshold before reading the result. A good experiment plan says what would count as a win, what would count as a regression, and what operational checks must pass before a launch can be trusted.

Do not launch from a single attractive metric in isolation. A/B decisions should consider the primary metric, confidence interval, p-value or posterior uncertainty, sample ratio mismatch, guardrails, segment effects, and practical business impact.

## Validity Checks

Sample ratio mismatch, missing exposure events, bot or abuse traffic, eligibility drift, and unbalanced treatment-control covariates can make an experiment unreliable. When validity checks fail, investigate instrumentation and assignment before interpreting metric lift.

Novelty effects can make short-term engagement look stronger than durable user value. For recommendation, search, ads, and marketplace ranking changes, consider whether a longer observation window is needed before launch.

## Metric Interpretation

Statistical significance is not the same as product significance. A tiny lift can be statistically significant but not worth operational risk. A large apparent lift can be untrustworthy if the experiment failed validity checks or if the confidence interval is wide.

Use confidence intervals to express uncertainty. When the confidence interval includes meaningful downside on a critical metric, avoid a full launch unless leadership explicitly accepts that risk.

