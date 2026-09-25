#!/usr/bin/env python3
"""Build n8n/agent-workflow.json: an importable n8n workflow with rules + knowledge embedded.

Flow: Chat Trigger → Detect language (Code) → Guard (Code: limits) → Allowed? (IF)
        → yes: Build prompt (Code) → AI Agent (Claude + memory) → Response (Set)   [error → Fallback reply]
        → no:  Limit reply (Set), Claude is not called
Run scripts/build_knowledge.py first. Re-run both after editing public/ or agent/rules.md,
then replace the "Build prompt" node code in n8n (or re-import).
"""
import json
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Response.output: never send an empty bubble (e.g. if the model stops before writing any text)
EMPTY_SAFE_OUTPUT = (
    '={{ ($json.output || "").trim() || ({'
    'ru: "Не получилось сформулировать ответ. Попробуйте спросить иначе или напишите Вильдане напрямую: меню «Let\'s talk» вверху страницы.", '
    'de: "Leider konnte ich keine Antwort formulieren. Bitte fragen Sie etwas anders oder schreiben Sie Vildana direkt über „Let\'s talk“ oben auf der Seite.", '
    'en: "Sorry, I couldn\'t put an answer together. Please rephrase the question or contact Vildana directly via “Let\'s talk” at the top of the page."'
    '})[$(\'Detect language\').item.json.reply_language] }}'
)
RULES = (ROOT / "agent" / "rules.md").read_text(encoding="utf-8")
KNOWLEDGE = (ROOT / "agent" / "knowledge.md").read_text(encoding="utf-8")
DETECT = (ROOT / "n8n" / "detect-language.js").read_text(encoding="utf-8")
DETECT = DETECT.replace("if (typeof module !== 'undefined') module.exports = { detectLanguage };\n", "")
GUARD = (ROOT / "n8n" / "guard.js").read_text(encoding="utf-8")
GUARD = GUARD.replace("if (typeof module !== 'undefined') module.exports = { guard, MAX_PER_SESSION, MAX_PER_DAY, MAX_CHARS };\n", "")

BUILD_PROMPT = """// Rules + knowledge are embedded here. To update: rebuild from the second-brain repo and paste again.
const RULES = %s;
const KNOWLEDGE = %s;

const j = $input.item.json;
const channel = j.channel || 'web';
const system_prompt = [
  RULES,
  '<knowledge>\\n' + KNOWLEDGE + '\\n</knowledge>',
  'channel: ' + channel,
  'Today: ' + new Date().toISOString().slice(0, 10),
  'REPLY LANGUAGE: ' + j.reply_language_name + '. Write every sentence in this language. Keep only names and technology names untranslated.',
].join('\\n\\n');

return { json: { ...j, channel, system_prompt } };
""" % (json.dumps(RULES, ensure_ascii=False), json.dumps(KNOWLEDGE, ensure_ascii=False))

FALLBACK_CODE = """// Runs when the AI Agent fails (e.g. Anthropic credit balance is empty, API down).
// Visitors get a polite answer in their language instead of an error.
const lang = $('Detect language').item.json.reply_language || 'en';
const TEXT = {
  ru: 'Извините, ассистент сейчас недоступен. Напишите Вильдане напрямую: кнопка «Let\\'s talk» вверху страницы.',
  de: 'Entschuldigung, der Assistent ist gerade nicht erreichbar. Bitte kontaktieren Sie Vildana direkt über „Let\\'s talk“ oben auf der Seite.',
  en: "Sorry, the assistant is unavailable right now. Please reach Vildana directly via “Let's talk” at the top of the page.",
};
// The error itself stays in the n8n execution log; visitors get only the text and the language.
return { json: { output: TEXT[lang] || TEXT.en, lang } };
"""

nid = lambda: str(uuid.uuid4())
TRIGGER, DETECT_N, PROMPT_N, AGENT, MODEL, MEMORY, RESP = (
    "When chat message received", "Detect language", "Build prompt", "AI Agent",
    "Claude", "Memory", "Response")
FALLBACK = "Fallback reply"
GUARD_N, ALLOWED, LIMIT = "Guard", "Allowed?", "Limit reply"

workflow = {
    "name": "Ask about Vildana (agent)",
    "nodes": [
        {
            "id": nid(), "name": TRIGGER, "type": "@n8n/n8n-nodes-langchain.chatTrigger", "typeVersion": 1.1,
            "position": [0, 0], "webhookId": nid(),
            "parameters": {"public": True, "mode": "webhook",
                           "options": {"allowedOrigins": "https://vildanarazumova.github.io", "responseMode": "lastNode"}},
        },
        {
            "id": nid(), "name": DETECT_N, "type": "n8n-nodes-base.code", "typeVersion": 2,
            "position": [240, 0],
            "parameters": {"mode": "runOnceForEachItem", "jsCode": DETECT},
        },
        {
            "id": nid(), "name": GUARD_N, "type": "n8n-nodes-base.code", "typeVersion": 2,
            "position": [480, 0],
            "parameters": {"mode": "runOnceForEachItem", "jsCode": GUARD},
        },
        {
            "id": nid(), "name": ALLOWED, "type": "n8n-nodes-base.if", "typeVersion": 2.2,
            "position": [720, 0],
            "parameters": {
                "conditions": {
                    "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
                    "conditions": [{"id": nid(), "leftValue": "={{ $json.blocked }}", "rightValue": "",
                                    "operator": {"type": "boolean", "operation": "false", "singleValue": True}}],
                    "combinator": "and",
                },
                "options": {},
            },
        },
        {
            "id": nid(), "name": LIMIT, "type": "n8n-nodes-base.set", "typeVersion": 3.4,
            "position": [960, 400],
            "parameters": {
                "assignments": {"assignments": [
                    {"id": nid(), "name": "output", "value": "={{ $json.limit_reply }}", "type": "string"},
                    {"id": nid(), "name": "lang", "value": "={{ $json.reply_language }}", "type": "string"},
                ]},
                "options": {},
            },
        },
        {
            "id": nid(), "name": PROMPT_N, "type": "n8n-nodes-base.code", "typeVersion": 2,
            "position": [960, 0],
            "parameters": {"mode": "runOnceForEachItem", "jsCode": BUILD_PROMPT},
        },
        {
            "id": nid(), "name": AGENT, "type": "@n8n/n8n-nodes-langchain.agent", "typeVersion": 2.2,
            "position": [1200, 0],
            "onError": "continueErrorOutput",
            "parameters": {
                "promptType": "define",
                "text": "={{ $json.chatInput }}\n\n[Reply language: {{ $json.reply_language_name }}]",
                "options": {"systemMessage": "={{ $json.system_prompt }}", "maxIterations": 3,
                            "enableStreaming": False},
            },
        },
        {
            "id": nid(), "name": MODEL, "type": "@n8n/n8n-nodes-langchain.lmChatAnthropic", "typeVersion": 1.3,
            "position": [1120, 220],
            "parameters": {
                "model": {"__rl": True, "mode": "id", "value": "claude-sonnet-5"},
                "options": {"maxTokensToSample": 1500, "temperature": 0.2},   # answers are short; headroom so a long think never ends in an empty reply
            },
        },
        {
            "id": nid(), "name": MEMORY, "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow", "typeVersion": 1.3,
            "position": [1280, 220],
            "parameters": {"contextWindowLength": 8},
        },
        {
            "id": nid(), "name": RESP, "type": "n8n-nodes-base.set", "typeVersion": 3.4,
            "position": [1520, 0],
            "parameters": {
                "assignments": {"assignments": [
                    {"id": nid(), "name": "output", "value": EMPTY_SAFE_OUTPUT, "type": "string"},
                    {"id": nid(), "name": "lang", "value": "={{ $('Detect language').item.json.reply_language }}",
                     "type": "string"},
                ]},
                "options": {},
            },
        },
        {
            "id": nid(), "name": FALLBACK, "type": "n8n-nodes-base.code", "typeVersion": 2,
            "position": [1520, 200],
            "parameters": {"mode": "runOnceForEachItem", "jsCode": FALLBACK_CODE},
        },
    ],
    "connections": {
        TRIGGER: {"main": [[{"node": DETECT_N, "type": "main", "index": 0}]]},
        DETECT_N: {"main": [[{"node": GUARD_N, "type": "main", "index": 0}]]},
        GUARD_N: {"main": [[{"node": ALLOWED, "type": "main", "index": 0}]]},
        ALLOWED: {"main": [[{"node": PROMPT_N, "type": "main", "index": 0}],
                           [{"node": LIMIT, "type": "main", "index": 0}]]},
        PROMPT_N: {"main": [[{"node": AGENT, "type": "main", "index": 0}]]},
        AGENT: {"main": [[{"node": RESP, "type": "main", "index": 0}],
                         [{"node": FALLBACK, "type": "main", "index": 0}]]},
        MODEL: {"ai_languageModel": [[{"node": AGENT, "type": "ai_languageModel", "index": 0}]]},
        MEMORY: {"ai_memory": [[{"node": AGENT, "type": "ai_memory", "index": 0}]]},
    },
    "settings": {"executionOrder": "v1"},
    "pinData": {},
}

out = ROOT / "n8n" / "agent-workflow.json"
out.write_text(json.dumps(workflow, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{out}: {out.stat().st_size:,} bytes")
