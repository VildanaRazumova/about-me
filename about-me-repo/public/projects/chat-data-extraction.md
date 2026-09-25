---
title: Recovering booking agreements buried in chat history
short_name: Chat records
summary: Turned free-form chat messages into a structured, checkable registry of booking agreements for the operations team, and mapped which exchanges could be automated next
kind: work
company: Fun&Sun
status: completed; the operations team worked from the registry
role: sole author, end-to-end
period: 2026-07
skills: [Python, text parsing, information extraction, data privacy, API access to corporate chat]
---

## Situation and task
Some booking terms existed only as free-text chat messages, without a template. The operations team needed them fast, as a structured list they could check and act on.

## What I did
- Organised the chat export so that each person exported their own chats, without a shared account.
- Extracted the key fields of each agreement into a registry.
- Kept the raw messages and the registry out of any code repository; only the code and written findings were saved.
- Used the same material to map which kinds of exchanges could be automated later.

### Key decisions
- Traceability over cleverness: every value links back to its source message, so nobody has to trust the parser blindly.
- Survey the formats before writing parser rules: the real patterns were narrower than expected, which saved a parser rewrite.

## Result
- The operations team worked from the registry. When the full chat history became available, the export was rebuilt and the number of recovered agreements roughly doubled.

## What I learned
- Even a one-off task needs a written problem statement.
- Defaults quietly change scope: an open end date let in messages from outside the agreed period.

## Good to discuss
Getting reliable, checkable data out of human conversation, and handling private messages responsibly.
