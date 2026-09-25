# Промпт: собрать карточку проекта из рабочего репозитория

**Как пользоваться**
1. Открой Claude Code **в корне рабочего репозитория** и включи plan mode (Shift+Tab дважды). Так Claude сначала покажет план и ничего не будет трогать без твоего согласия.
2. Замени три значения в `<<...>>` и вставь промпт целиком.
3. Сначала прочитай `REVIEW.md` и ответь на вопросы. Карточку `public/…` переноси в second brain только после этого.
4. Повтори для каждого репозитория. Один репозиторий — одна карточка. Если в репо несколько проектов, получится несколько карточек.

Страховка: подключи хук `check_public.sh` из проекта (PreToolUse на Write/Edit). Тогда внутренние термины физически не попадут в `public/`, даже если Claude ошибётся.

---

```text
You are helping me write an honest, public-safe portfolio card about my work in THIS repository.
The card will be read by an AI assistant that answers recruiters and companies about me, so it must be
(1) free of confidential information and (2) specific and evidence-backed, so the assistant never has to guess.

## Settings
- MY_GIT_AUTHOR: <<my git author name or email, e.g. "Vildana">>
- OUTPUT_DIR: <<absolute path to my second-brain folder, e.g. ~/about-me>>
- EMPLOYER_PUBLIC_NAME: "Fun&Sun" (first mention: <<company_first_mention from facts.yaml>>). Never use any other name for the employer.

## Hard rules: safety
1. READ-ONLY. Do not modify, commit, push, install, or run anything in this repo. Do not run code that touches databases, APIs or the network.
2. Do NOT open secret files: .env*, *secret*, *credential*, *.pem, *.key, *token*, password-manager or vault exports, or any config that contains passwords or keys. If you see a secret by accident, never quote it anywhere.
3. Nothing below may appear in any output file, not even in the private notes:
   - hostnames, URLs, IPs, ports, internal domains, webhook paths
   - database, schema, table, view, bucket or queue names (say "the analytical warehouse" instead)
   - credentials, tokens, service-account names, ticket or project keys
   - names of colleagues, managers, clients, partners, suppliers, competitors
   - internal system and vendor platform names (say "the booking platform", "an industry pricing API", "competitor websites")
   - prices, margins, revenue, budgets, booking counts, volumes that reveal the size of the business, internal KPIs
   - personal data of any kind (customers, employees), raw data samples, screenshots
   - the employer's legal entity or any name other than EMPLOYER_PUBLIC_NAME
   Public technologies are fine and wanted: Python, LightGBM, FastAPI, Claude API, Docker, etc.
4. Order-of-magnitude is fine only when it describes the ENGINEERING, not the business: "~170k rows of historical data" is OK,
   "we sell 12,400 tours a month" is not. If unsure, leave it out and add it as a question.

## Hard rules: truthfulness
5. Every statement in the card must be supported by something you actually opened in this repo: code, README, docs, notebooks
   (including their saved outputs), configs, schedules (cron, n8n workflow exports, Airflow DAGs, CI), or git history.
   File names alone are not evidence. Open the file.
6. Separate MY work from other people's. Use `git log --author="MY_GIT_AUTHOR"`, `git shortlog -sn`, and the files I touched.
   If others contributed, describe only my part. If authorship is unclear, ask.
7. Status must come from evidence:
   - production = scheduled/deployed and running (schedule/deploy config + recent run logs or commits that show operation)
   - pilot = running for a limited scope or audience
   - prototype = works end-to-end but is not operated regularly
   - design = docs/specs, little or no working code
   If you can't tell, write "⚠ status unclear" and ask.
8. Metrics: only numbers that literally appear in the repo (notebook outputs, reports, logs), each with its evaluation setup
   (holdout / CV / backtest, period). Never invent or estimate business impact. If no impact was measured, say so plainly.
9. No superlatives, no marketing language, no "significantly improved". Plain verbs: built, designed, tested, deployed, replaced.
9a. Name the project by what it does for a non-technical reader. Never use internal codenames, version numbers,
    bot nicknames or team slang ("Atlas 2.0", "HelperBot", "Project Falcon"). The same applies inside the text: say
    "the pricing model", not the internal module or repo name.
10. When information is missing, do NOT fill the gap. Add a question for me instead.

## Process
Step 1. Inventory (read-only). List what the repo contains: purpose, main modules, entry points, pipelines and schedules,
        notebooks, tests, docs, dependencies. Show me this inventory and your plan before writing anything.
Step 2. Git facts. My commit count and share, first and last commit dates, areas I worked on (directories/modules).
Step 3. Write OUTPUT_DIR/private/repo-notes/<repo-slug>.md: a detailed evidence log. Each claim goes on one line:
        claim → evidence (file path, notebook cell, or commit hash + date). Evidence = paths and hashes only, never pasted content.
Step 4. Write OUTPUT_DIR/public/projects/<project-slug>.md using EXACTLY this template (English, max ~350 words).
        The sections follow STARR (Situation/Task → Action → Result → Reflection), the structure recruiters use in structured interviews.
        If the repo contains several independent projects, write one card per project.

---
title: <plain-language description of what it does, 4–8 words, e.g. "Automatic pricing for package tours">
short_name: <2–3 words for inline citations, e.g. "Tour pricing">
summary: <one sentence a non-technical reader understands>
company: Fun&Sun
status: <production | pilot | prototype | design>, <short detail>
role: <my role, e.g. "sole data scientist, end-to-end">
period: <YYYY-MM – YYYY-MM or "ongoing">
stack: [<public technologies only>]
cv_line: <one CV bullet by the XYZ formula: "Built X that achieved Y, by doing Z". Y is a real number with its evaluation setup, or an observable fact ("runs in production 3× a day"). Never an estimate.>
evidence: []   # optional: public links (repo, article, slides)
---

## Situation and task
<2–3 sentences: the business problem in generic terms and what I was responsible for. At most ~25% of the card.>

## What I did
<The longest section, about half of the card. 3–6 bullets in first person ("I built…", "I designed…"). Only my own part; mention the team where relevant.>

### Key decisions
<2–3 bullets: "I chose X instead of Y because Z" — the constraint or business goal behind it. Only if visible in the repo/docs; otherwise ask me.>

## Result
<Status in plain words. Metrics with their evaluation setup, or a concrete qualitative outcome (what is used, by whom, how often). If business impact was not measured: "Business impact has not been measured yet.">

## What I learned
<2–3 bullets: the lesson and where I applied it afterwards. Only real lessons visible in the repo history or docs; otherwise ask me.>

Step 5. Self-check before you finish. Go through the public card sentence by sentence:
        (a) point to the evidence line in the private notes. If there is none, delete the sentence.
        (b) scan for anything from rule 3. Also run:
            grep -vE '^\s*(#|$)' OUTPUT_DIR/private/stopwords.txt > /tmp/stopwords && grep -niE -f /tmp/stopwords <card>
        (c) check that status, role and every number match the evidence.
        Report what you removed and why.
Step 6. Write OUTPUT_DIR/private/repo-notes/<repo-slug>.REVIEW.md with:
        - up to 7 questions for me (only things the repo cannot answer: business context, impact, my exact role, status)
        - a list of anything you were unsure is safe to publish
        - suggested additions to OUTPUT_DIR/private/stopwords.txt (internal names you found in the repo)
        - candidate interview stories visible in the repo history (a rewrite, a rejected approach, an incident, a big fix):
          one line each + what you need from me to turn it into a STARR story
```
