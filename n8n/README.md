# The n8n workflow, node by node

`agent-workflow.json` is the full export (credentials removed). Import it into n8n, attach an Anthropic credential to the **Claude** node, and publish.

| Node | Type | What it does |
|---|---|---|
| When chat message received | Chat Trigger (webhook, public) | Receives `{ chatInput, sessionId, channel, lang_hint, prev_lang }` from the page. `allowedOrigins` is set to the site's origin. |
| Detect language | Code (`detect-language.js`) | Decides `reply_language` (ru / de / en) from the visitor's own words: first sentence, then whole text, then previous reply language, then browser language, else English. |
| Guard | Code (`guard.js`) | Per-session and daily counters in workflow static data; message length cap. Sets `blocked`, `limit_reply`. |
| Allowed? | IF | `blocked == false` → Build prompt; otherwise → Limit reply. |
| Limit reply | Set | Returns the polite limit message in the visitor's language. The model is not called. |
| Build prompt | Code | Holds `RULES` (agent/rules.md) and `KNOWLEDGE` (built from public/) as string constants and assembles the system prompt: rules, `<knowledge>…</knowledge>`, channel, today's date, reply language. |
| AI Agent | LangChain Agent | Sends the system prompt and the visitor's message to the model. No tools attached. `maxIterations: 3`. |
| Claude | Anthropic chat model | `claude-sonnet-5`, temperature 0.2, max 1,500 output tokens. |
| Memory | Window buffer memory | Last 8 messages per `sessionId`. |
| Response | Set | `{ output, lang }`. If the model returned an empty answer, a short fallback text in the visitor's language. |
| Fallback reply | Code | On AI Agent error (API down, no credit): apology in the visitor's language. Error details stay in the execution log. |

## Notes

- Counters in `Guard` use `$getWorkflowStaticData('global')`, which persists only for the published (production) workflow, not for test runs in the editor.
- The knowledge is embedded as a constant on purpose: one file to review, no runtime fetches, no vector store. `scripts/build_workflow.py` regenerates the export; in a live instance the `Build prompt` code is patched and the workflow re-published.
- Set an execution-data retention (e.g. `EXECUTIONS_DATA_PRUNE=true`, `EXECUTIONS_DATA_MAX_AGE=168`) so visitors' questions are not kept forever.
