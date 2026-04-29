# Sample Ratio Mismatch

## Definition

Sample ratio mismatch, or SRM, occurs when the observed allocation between experiment groups differs materially from the planned allocation. In a 50/50 experiment, a 70/30 split is a severe warning sign.

## Why SRM Matters

SRM can indicate randomization bugs, eligibility filtering, exposure logging loss, bot traffic, instrumentation joins, or analysis mistakes. When SRM occurs, treatment and control may no longer be comparable. Apparent metric lifts can be artifacts of the mismatch.

## Launch Rule

If SRM fails at a strict threshold such as p < 0.01, do not trust the experiment result. Do not launch because revenue appears higher. First investigate assignment, exposure logging, eligibility rules, and data joins. Re-run the experiment if needed.

## Debug Checklist

Check the expected traffic split, assignment service logs, exposure event counts, experiment eligibility filters, platform or country exclusions, bot filtering, missing user IDs, and time-window alignment. Compare SRM by device, country, app version, and user segment to locate the source.

## Memo Language

Use direct language: "The experiment has sample ratio mismatch, so the measured treatment lift is not valid launch evidence." Avoid softening the issue as a minor caveat when allocation is badly imbalanced.

