---
title: A chat assistant that tells staff whether a payment has arrived
short_name: Payments assistant
summary: An internal chat assistant that answers staff questions about whether a payment has arrived, instead of sending each question to the finance team
kind: work
company: Fun&Sun
status: in production since July 2026 for internal staff
role: designed and built it (main author)
period: 2026-07 – 2026-08
skills: [Python, Dify, LLM applications, API design, access control, evaluation of LLM systems]
---

## Situation and task
The finance team got a constant stream of routine questions: has this payment arrived? The task: let staff get these answers themselves, safely.

## What I did
- Analysed 6 months of chat history, grouped the questions and wrote scenarios; we chose the main one, payment status, to automate first.
- Built the assistant on Dify (an LLM application platform) in Microsoft Teams: staff ask about the payment status of a booking.
- If there is a problem, it offers to open a Jira ticket routed to the right team.

### Key decisions
- Analysis before code: most past questions were about work already done, so the answer was in the data, just not visible to the person asking; this set the scope.
- No open-ended queries: the assistant reads company data only through a small set of reviewed functions, so it stays predictable and testable.
- Permissions as a core part from the start, tested separately: each employee sees only what they are entitled to.
- Quality checked automatically on a fixed set of test questions before every change, not judged by impressions.

## Result
- In production since mid-July 2026 for internal staff. The effect on the finance team's workload has not been measured yet.

## What I learned
- In an assistant over financial data, permissions matter as much as the answers.

## Good to discuss
Putting an LLM assistant in front of sensitive business data safely. Architecture details stay internal to Fun&Sun.
