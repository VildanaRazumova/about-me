// n8n Code node ("Run Once for Each Item"), placed right after the Chat Trigger / Telegram Trigger.
// Detects the reply language (ru / de / en) from the visitor's OWN words, deterministically,
// so the LLM never has to guess. Output fields go into the AI Agent's system message:
//   ...rules + knowledge...
//   REPLY LANGUAGE: {{ $json.reply_language_name }}. Write every sentence in this language.
//
// Fallback chain when the text itself has too little signal ("ok", "Hi", a link):
//   prev_lang (language of the previous turn, sent by the web page) → hint (browser language /
//   Telegram message.from.language_code) → English.

const DE = new Set(('der die das und ist nicht sie ich wir ein eine einen mit für auf wie hat haben sind zu den dem ' +
  'auch kann können bitte über ihr ihre welche welcher warum wer gibt es noch mehr oder aber bei von nach ' +
  'stelle erfahrung arbeitet gebaut projekt projekte hallo danke guten tag servus erzählen sie mir diese dieser ' +
  'kenntnisse deutsch passt woran arbeitet gerade').split(' '));
const EN = new Set(('the and is are not she he i we a an with for on how what has have to of it can please about ' +
  'her which why who does did there more or but at from this that built work working experience role hi hello ' +
  'thanks thank yes tell me job position fit would could should').split(' '));

function scoreOf(s) {
  const cyr = (s.match(/[а-яё]/gi) || []).length;
  const lat = (s.match(/[a-zäöüß]/gi) || []).length;
  const words = s.toLowerCase().match(/[a-zäöüß]+/g) || [];
  let de = 0, en = 0;
  for (const w of words) { if (DE.has(w)) de++; if (EN.has(w)) en++; }
  de += ((s.match(/[äöüß]/gi) || []).length) * 2;
  return { cyr, lat, de, en, n: words.length };
}

function decide(s) {
  const x = scoreOf(s);
  if (x.cyr >= 3 && x.cyr >= x.lat * 0.3) return 'ru';
  const need = x.n <= 3 ? 1 : 2;           // short messages: one clear word is enough
  if (Math.max(x.de, x.en) < need || x.de === x.en) return null;
  return x.de > x.en ? 'de' : 'en';
}

function detectLanguage(text, prevLang, hint) {
  const t = String(text || '').trim();
  // the visitor's own words usually come first: first sentence (or line), then the whole text
  const head = (t.match(/^[\s\S]{3,200}?[?!.\n]/) || [t.slice(0, 200)])[0];
  const norm = (l) => (l || '').toLowerCase().slice(0, 2);
  return decide(head) || decide(t) ||
    (['ru', 'de', 'en'].includes(norm(prevLang)) ? norm(prevLang) : null) ||
    (['ru', 'de', 'en'].includes(norm(hint)) ? norm(hint) : null) || 'en';
}

const NAMES = { ru: 'Russian (русский)', de: 'German (Deutsch, formal "Sie")', en: 'English' };

// ── n8n glue ────────────────────────────────────────────────────────
if (typeof $input !== 'undefined') {
  const j = $input.item.json;
  const text = j.chatInput ?? j.message?.text ?? '';
  const hint = j.lang_hint ?? j.message?.from?.language_code ?? '';
  const lang = detectLanguage(text, j.prev_lang, hint);
  return { json: { ...j, reply_language: lang, reply_language_name: NAMES[lang] } };
}

if (typeof module !== 'undefined') module.exports = { detectLanguage };
