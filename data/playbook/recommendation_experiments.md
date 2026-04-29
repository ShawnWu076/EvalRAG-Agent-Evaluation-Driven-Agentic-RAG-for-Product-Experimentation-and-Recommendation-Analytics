# Recommendation Experiments

## Recommendation-Specific Risks

Recommendation and ranking systems can create tradeoffs between immediate engagement and durable user value. A model may increase CTR or revenue by making the feed more sensational, repetitive, or commercially aggressive. These changes can hurt retention, user trust, content diversity, or creator ecosystem health.

## Primary Metrics

Common primary metrics include revenue per user, CTR, conversion rate, watch time, saves, add-to-cart rate, and qualified engagement. The primary metric should match the product goal. For commerce recommendations, conversion quality and revenue often matter more than clicks alone.

## Guardrails

Recommendation experiments should usually check 7-day retention, 28-day retention when available, complaint or hide rate, latency, diversity, and high-value user impact. If the model improves short-term metrics but retention declines, do not fully launch without understanding the tradeoff.

## Segment Analysis

Analyze new users, returning users, high-value users, low-activity users, device type, country, traffic source, and content or item category. Segment analysis is not a fishing expedition when it is tied to known product risks and launch guardrails.

## CTR Up, Conversion Down

CTR increases can be misleading when conversion rate or revenue per click decreases. That pattern often means the system is attracting lower-quality clicks or moving users into items they do not actually buy. Do not launch a recommendation model based only on CTR when downstream quality metrics degrade.

