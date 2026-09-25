---
title: "Working as the only data scientist: AI reviewers and a second brain per project"
short_name: Working method
summary: A "second brain" for each project, and AI assistants for review, testing, documentation and business explanations, so knowledge never depends on one person
kind: work
company: Fun&Sun
status: in daily use; a working method, not a product
role: author of the method
period: 2026-05 – ongoing
skills: [Claude Code, code review, testing, documentation, workflow automation]
---

## Situation and task
I am the only data scientist on several products, so no colleague reviews my code or shares the documentation. The task: keep quality and knowledge from depending on one person's memory.

## What I did
- Use AI assistants with separate roles: code review, checking results, explaining logic in business language.
- Run every production change through a fixed quality gate: tests, review and data checks.
- Keep a "second brain" per project (key decisions, meeting notes, status); the AI assistants work from it, and new people can start without me.
- Share project documents in a SharePoint space with "explain it to the business" instructions, so stakeholders can ask Claude or ChatGPT about a project in their own words.
- Run scheduled monitoring to catch silent failures early.

### Key decisions
- Several reviewers with separate roles, not one general reviewer: they find more.
- Checks that try to break things on purpose: a check that always passes teaches nothing.

## Result
- In daily use; every change has a written review trail.
- The business trusts that knowledge will not leave with one person, and stakeholders get answers without waiting for a meeting. Time saved has not been measured.

## Good to discuss
Keeping review discipline and documentation without a second engineer, and making technical projects clear to the business.
