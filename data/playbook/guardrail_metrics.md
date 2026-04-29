# Guardrail Metrics

## Definition

A guardrail metric is a metric that should not meaningfully degrade while the team optimizes the primary objective. Guardrails protect long-term user value, marketplace health, trust, safety, and business quality from short-term metric gaming.

## Common Guardrails

For recommendation systems, common guardrails include retention, session quality, complaint rate, hide rate, report rate, unsubscribe rate, latency, content diversity, creator or seller health, and long-term value. For ads systems, guardrails include advertiser ROI, conversion quality, ad load, user complaints, and policy violations.

## Launch Rule

Do not fully launch when a critical guardrail metric significantly worsens, even if revenue, CTR, or another primary metric improves. A guardrail failure usually means the team should investigate, redesign, restrict rollout, or extend the experiment.

When a guardrail movement is small but uncertain, inspect confidence intervals, segment effects, and practical risk. If the plausible downside is material, treat the result as unresolved rather than a clean win.

## Retention Guardrail

Retention is especially important for recommendation and feed-ranking experiments. A model can increase clicks, watch time, or short-term revenue by showing more aggressive content while making users less likely to return. When 7-day or 28-day retention drops, the launch decision should become conservative.

## Complaint and Trust Guardrails

Complaint, hide, report, unsubscribe, and refund metrics often move at low base rates. Small absolute changes can still matter because they indicate quality or trust damage. If these metrics worsen, inspect segments, content categories, and exposure frequency before launch.

