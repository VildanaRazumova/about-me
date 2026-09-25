---
title: Which requests should a bot answer? A mailbox analysis
short_name: Mailbox analysis
summary: Analysed requests to shared mailboxes, worked out which scenarios an assistant should handle, and built the most valuable one as the Payments assistant
kind: work
company: Fun&Sun
status: completed; the scenarios were implemented in the Payments assistant
role: "data scientist, end-to-end: analysis, scenario design, then the assistant itself"
period: 2026-07
skills: [Python, NLP, LLM classification, personal-data protection, scenario design]
---

## Situation and task
Several shared mailboxes get many repetitive requests. Before building anything, the team needed to know what actually arrives, what a machine could answer, and what must stay with people.

## What I did
- Collected several months of requests, removed personal data before any analysis, and sorted them by topic, problem and resolution.
- Turned the categories into scenarios: what the assistant answers itself, what it clarifies, what it hands to a person.
- Compared an LLM platform with custom code, and chose the platform.
- Built the most valuable scenario, payment-status questions, as the Payments assistant on Dify.

### Key decisions
- Measure before automating: the category split changed the plan more than any modelling choice.
- A separate quality check for privacy protection, because a missed piece of personal data is an incident, not a bug.

## Result
- Automation scenarios backed by data; the first one is in production as the Payments assistant.

## Good to discuss
Turning a messy flow of requests into concrete automation scenarios, under privacy constraints.
