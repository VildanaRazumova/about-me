// n8n Code node "Guard" ("Run Once for Each Item"), placed right after "Detect language".
// Protects the Anthropic budget on a public chat: the question goes to Claude only if
//   - the message is not too long,
//   - this conversation (sessionId) has not used up its questions for today,
//   - the whole assistant has not used up its questions for today (sessionIds are set by the browser,
//     so an attacker could invent new ones — the daily total is the real brake).
// Counters live in the workflow's static data: they are saved only for production runs of the
// published workflow (not for test-chat runs in the editor) and reset every day (UTC).

const MAX_PER_SESSION = 20;    // questions per conversation per day
const MAX_PER_DAY = 100;       // questions for the whole assistant per day (≈ $3.5 at ~3.5¢ each)
const MAX_CHARS = 1500;        // a question or the key requirements of a job, not a full vacancy

const TEXT = {
  session: {
    ru: 'Спасибо за интерес! В этом разговоре закончился лимит вопросов. Чтобы продолжить, напишите Вильдане напрямую: меню «Let\'s talk» вверху страницы.',
    de: 'Vielen Dank für Ihr Interesse! Das Fragenlimit für dieses Gespräch ist erreicht. Bitte schreiben Sie Vildana direkt über „Let\'s talk“ oben auf der Seite.',
    en: "Thanks for your interest! This conversation has reached its question limit. To continue, please contact Vildana directly via “Let's talk” at the top of the page.",
  },
  daily: {
    ru: 'Сегодня ассистент уже ответил на много вопросов и отдыхает до завтра. Напишите Вильдане напрямую: меню «Let\'s talk» вверху страницы.',
    de: 'Der Assistent hat heute schon viele Fragen beantwortet und ist ab morgen wieder da. Bitte schreiben Sie Vildana direkt über „Let\'s talk“ oben auf der Seite.',
    en: "The assistant has answered many questions today and will be back tomorrow. Please contact Vildana directly via “Let's talk” at the top of the page.",
  },
  too_long: {
    ru: 'Сообщение слишком длинное. Пожалуйста, сократите его до 1500 символов: для вакансии достаточно ключевых требований.',
    de: 'Die Nachricht ist zu lang. Bitte kürzen Sie sie auf 1.500 Zeichen: Für eine Stelle genügen die wichtigsten Anforderungen.',
    en: 'The message is too long. Please keep it under 1,500 characters: for a job, the key requirements are enough.',
  },
};

function guard(j, store) {
  const today = new Date().toISOString().slice(0, 10);
  if (store.day !== today) { store.day = today; store.total = 0; store.sessions = {}; }
  // Migration of counters written before the 's:' prefix (v1.2, 2026-09-25): merge them, so a conversation keeps its count.
  for (const k of Object.keys(store.sessions)) {
    if (k.startsWith('s:')) continue;
    const nk = 's:' + k;
    store.sessions[nk] = (Object.prototype.hasOwnProperty.call(store.sessions, nk) ? store.sessions[nk] : 0) + store.sessions[k];
    delete store.sessions[k];
  }
  const sid = 's:' + String(j.sessionId || 'anonymous').slice(0, 64);   // prefixed key: 'constructor' / '__proto__' cannot escape the per-session cap
  const used = Object.prototype.hasOwnProperty.call(store.sessions, sid) ? store.sessions[sid] : 0;
  const text = String(j.chatInput ?? j.message?.text ?? '');

  let reason = null;
  if (text.length > MAX_CHARS) reason = 'too_long';
  else if (store.total >= MAX_PER_DAY) reason = 'daily';
  else if (used >= MAX_PER_SESSION) reason = 'session';

  if (!reason) { store.sessions[sid] = used + 1; store.total += 1; }
  const lang = j.reply_language || 'en';
  return {
    ...j,
    blocked: Boolean(reason),
    block_reason: reason || '',
    limit_reply: reason ? (TEXT[reason][lang] || TEXT[reason].en) : '',
    questions_today: store.total,
  };
}

// ── n8n glue ────────────────────────────────────────────────────────
if (typeof $input !== 'undefined') {
  return { json: guard($input.item.json, $getWorkflowStaticData('global')) };
}

if (typeof module !== 'undefined') module.exports = { guard, MAX_PER_SESSION, MAX_PER_DAY, MAX_CHARS };
