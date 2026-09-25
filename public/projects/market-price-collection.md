---
title: Competitor price monitoring, automated through an external data API
short_name: Competitor price monitoring
summary: A daily pipeline, built on an external data API, that collects competitors' package-tour prices, so pricing can rely on data and history instead of manual website checks
kind: work
company: Fun&Sun
status: in production, collecting daily; now maintained by another team; used for analysis, not yet part of any price
role: designed and built the API integration and the pipeline end-to-end, then handed it over
period: 2026-08 – ongoing
skills: [Python, REST API integration, Airflow, data engineering, data-quality monitoring, testing]
---

## Situation and task
The pricing team checked competitor prices by hand on websites: it took up most of their working day, no history was kept, and a price that disappears cannot be recovered later. The task: collect prices for comparable tours automatically, every day.

## What I did
- Integrated a paid external data API and designed the collection around its rate limits and budget.
- Planned the requests to cover every relevant route and date without gaps or duplicates; new destinations need only a configuration change.
- Built the daily collection with a run log and a completeness check.
- Built a like-for-like comparison of competitors' offers with the company's own.
- Added monitoring for silent failures, and tests that make no paid calls.

### Key decisions
- Small experiments first: the API behaved differently than expected, which changed the design and cut the planned cost substantially.
- Completeness first: a half-finished run is never used in an analysis.
- Handover planned from the start: a runbook and a decision log instead of knowledge in one head.

## Result
- The manual routine is gone, so the pricing team had time to test the new pricing system.
- In production, collecting daily and checked against the company's own figures; another team has maintained it since the handover.

## What I learned
- With a rate-limited API, small experiments beat assumptions.

## Good to discuss
Integrating an external data API within budget, and handing a system over to another team.
