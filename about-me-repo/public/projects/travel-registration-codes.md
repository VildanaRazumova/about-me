---
title: Registering every outbound tourist with a state service, automatically
short_name: Registration API
summary: An integration with a state service's API to register every outbound tourist automatically, with status tracking and a daily reconciliation
kind: work
company: Fun&Sun
status: ran daily in production until the process ended in July 2026
role: sole author, end-to-end
period: 2026-06 – 2026-07
skills: [Python, REST API integration, n8n, PostgreSQL, data reconciliation]
---

## Situation and task
Every outbound tourist had to be registered with a state service and get a code. By hand, this does not scale, and errors are a compliance problem. The task: automate the whole cycle through the service's API.

## What I did
- Generated the registration requests from booking and flight data, and handled the service's responses and statuses.
- Added retries, protection against duplicate registrations, and a daily reconciliation of requested against issued codes.
- Filled gaps in the source systems with standard reference data, such as airline and country codes.
- Scheduled the flows in n8n; when the process ended, documented the final state and how to restore it.

### Key decisions
- Reliability as the core of the product, not an extra: the service can fail or answer slowly, and no tourist may be missed silently.

## Result
- Ran daily in production until July 2026.

## What I learned
- In an API integration, most of the effort goes into data completeness and failure handling, not into the call itself.

## Good to discuss
An API integration where errors are a compliance problem, so correctness matters more than speed.
