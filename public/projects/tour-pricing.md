---
title: Price recommendations for package tours, with a reason for each
short_name: Tour pricing
summary: An ML-assisted system that suggests price changes for package tours and tells the pricing manager why, in plain language
kind: work
company: Fun&Sun
status: pilot — recommendations are advisory; managers decide, nothing is changed automatically
role: sole data scientist, end-to-end (data, model, rules and the managers' page)
period: 2026-03 – ongoing
skills: [Python, SQL, gradient boosting, explainable ML, time-series validation, workflow automation]
---

## Situation and task
Pricing managers adjusted tour prices by hand and spent most of their time looking up data instead of deciding. The task: give them recommendations they can trust and check.

## What I did
- Combined a machine-learning demand forecast with rules learned from managers' past pricing.
- Rebuilt past booking curves using only what was known at each point in time (no data leakage).
- Built the managers' page: each recommendation explains in plain words why the price should go up or down.
- Added safeguards: data checks before each run, alerts, and checks that a change does not break what already works.

### Key decisions
- Rules next to the model, not a black box: managers must explain every price to the business, so they need to follow and challenge each suggestion.
- Separate logic for the last weeks before departure, where demand behaves differently than months ahead.
- Stable prices: damping stopped forecast noise from making prices jump back and forth, without slowing the reaction to real demand shifts.

## Result
- Pilot: managers work with the recommendations; an A/B comparison in the next phase will measure business impact.
- In time-series validation, the forecast's error is about a third lower than a naive baseline.

## What I learned
- Adoption depends on explainability as much as on accuracy.

## Good to discuss
Explainable pricing recommendations and combining ML with business rules. Implementation details stay internal to Fun&Sun.
