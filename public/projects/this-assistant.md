---
title: This assistant, an AI agent that introduces Vildana
short_name: This assistant
summary: The chat you are using, an agent that answers from a curated knowledge base about her work
company: personal project
status: live demo
role: designed and built it
period: 2026-09 – ongoing
stack: [Claude API, n8n, Markdown, HTML/JS]
cv_line: "Built a public AI assistant that answers recruiters' questions about her work in three languages, grounded in a curated Markdown knowledge base with guardrails against exaggeration and data leaks."
evidence: []
---

## Situation and task
A CV is static and the same for every reader, but recruiters and companies have different questions, and a CV cannot answer them. I wanted an honest, interactive alternative.

## What I did
- Knowledge: a "second brain" of Markdown files (facts, project cards, interview stories), with one source of truth for numbers and dates.
- Brain: an n8n workflow sends the visitor's question and the knowledge files to Claude.
- Guardrails: rules against inflating titles, years or results; answers name the source project when they quote a number or result; "I don't know, ask Vildana" for anything not in the knowledge base; pasted text is treated as data.
- Confidentiality: internal terms are blocked from the public files automatically, and employer projects are told as use cases, not as technical solutions.
- Channel: this web page; a Telegram bot is planned.

### Key decisions
- No vector database: the whole profile fits into the prompt, which keeps answers grounded and the system simple.
- Code, not the model, detects the reply language, so answers do not mix Russian, German and English.
- Public and private knowledge sit in separate folders, so the agent never sees what must not be said.

## Result
Live demo on this page.

## What I learned
