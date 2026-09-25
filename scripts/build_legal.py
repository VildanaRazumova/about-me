#!/usr/bin/env python3
"""Builds site/privacy.html and site/impressum.html in the page's own style (tokens and self-hosted fonts
taken from site/index.html). German first, then English and Russian. No JavaScript, no external requests.

Decision 25.09.2026: the site is a personal portfolio, nothing is sold, so no Impressum is published and no postal
address appears (the privacy policy names the controller by name, country and e-mail). `--with-impressum` also builds
impressum.html with address placeholders, should that decision change.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
index = (SITE / "index.html").read_text(encoding="utf-8")

FONT_FACES = "\n".join(l for l in index.splitlines() if l.strip().startswith("@font-face"))
TOKENS = re.search(r"  :root \{.*?\n  \}\n  @media \(prefers-color-scheme: dark\) \{.*?\n  \}\n", index, re.S).group(0)

STAND = "25.09.2026"
EMAIL = "wildanka1@gmail.com"
WITH_IMPRESSUM = "--with-impressum" in sys.argv
ADDRESS_DE = "[Straße und Hausnummer], [PLZ Ort], Deutschland" if WITH_IMPRESSUM else "Deutschland"
ADDRESS_EN = "[Street and number], [Postcode City], Germany" if WITH_IMPRESSUM else "Germany"
ADDRESS_RU = "[улица и дом], [индекс, город], Германия" if WITH_IMPRESSUM else "Германия"

CSS = f"""
  {FONT_FACES}
{TOKENS}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; }}
  body {{ background: var(--bg); color: var(--ink); font: 15.5px/1.65 var(--sans); -webkit-font-smoothing: antialiased; }}
  a {{ color: var(--brand-ink); }}
  .top {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px max(16px, calc((100vw - 760px) / 2));
         border-bottom: 1px solid var(--line); background: color-mix(in srgb, var(--bg) 88%, transparent); }}
  .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 600; letter-spacing: -.01em; color: var(--ink); text-decoration: none; }}
  .mono {{ width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; background: var(--brand); color: #fff; font-size: 12px; font-weight: 600; }}
  .langs {{ display: flex; gap: 6px; font-size: 13px; }}
  .langs a {{ text-decoration: none; padding: 4px 10px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted); }}
  main {{ max-width: 760px; margin: 0 auto; padding: 28px 16px 56px; }}
  h1 {{ font: 600 30px/1.2 var(--serif); letter-spacing: -.01em; margin: 6px 0 4px; }}
  h2 {{ font: 600 17px/1.3 var(--sans); margin: 28px 0 8px; }}
  section + section {{ border-top: 1px solid var(--line); margin-top: 40px; padding-top: 8px; }}
  p, li {{ color: var(--ink); margin: 0 0 10px; }}
  .stand, .muted {{ color: var(--muted); font-size: 14px; }}
  dl {{ display: grid; grid-template-columns: max-content 1fr; gap: 6px 16px; margin: 0 0 10px; }}
  dt {{ color: var(--muted); }}
  dd {{ margin: 0; }}
  .fill {{ background: color-mix(in srgb, var(--accent) 22%, transparent); border-radius: 4px; padding: 0 4px; }}
  address {{ font-style: normal; }}
  footer {{ max-width: 760px; margin: 0 auto; padding: 16px; font-size: 13px; color: var(--muted); border-top: 1px solid var(--line); }}
  @media (max-width: 560px) {{ dl {{ grid-template-columns: 1fr; gap: 2px; }} dt {{ margin-top: 8px; }} }}
"""

def fill(s: str) -> str:
    return re.sub(r"\[([^\]]+)\]", r'<span class="fill">[\1]</span>', s)

def page(title: str, body: str, back: str) -> str:
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none'; style-src 'unsafe-inline'; img-src 'self'; font-src 'self'; connect-src 'none'; form-action 'none'; object-src 'none'; base-uri 'self'">
<meta name="robots" content="noindex">
<title>{title} — Vildana Razumova</title>
<style>{CSS}</style>
</head>
<body>
  <header class="top">
    <a class="brand" href="./"><span class="mono">VR</span> Vildana Razumova</a>
    <nav class="langs" aria-label="Sprache / Language / Язык"><a href="#de">Deutsch</a><a href="#en">English</a><a href="#ru">Русский</a></nav>
  </header>
  <main>
{body}
  </main>
  <footer><a href="./">{back}</a>{' · <a href="impressum.html">Impressum</a>' if WITH_IMPRESSUM else ''} · <a href="privacy.html">Datenschutz / Privacy / Конфиденциальность</a></footer>
</body>
</html>
"""

# ───────────────────────────── Datenschutzerklärung ─────────────────────────────
privacy_de = f"""
    <section id="de" lang="de">
      <h1>Datenschutzerklärung</h1>
      <p class="stand">Stand: {STAND}</p>

      <h2>1. Verantwortliche</h2>
      <p><address>Vildana Razumova, {fill(ADDRESS_DE)}<br>E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a></address></p>
      <p>Eine Datenschutzbeauftragte ist nicht bestellt; die gesetzlichen Voraussetzungen dafür liegen nicht vor.</p>

      <h2>2. Hosting und Server-Logfiles</h2>
      <p>Diese Website wird auf GitHub Pages gehostet (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). Beim Aufruf verarbeitet GitHub technisch notwendige Verbindungsdaten, insbesondere die IP-Adresse, Datum und Uhrzeit des Zugriffs sowie Angaben zu Browser und Betriebssystem. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse am sicheren und störungsfreien Betrieb der Seite). Die Übermittlung in die USA stützt sich auf die Zertifizierung von GitHub nach dem EU-U.S. Data Privacy Framework.</p>

      <h2>3. Schriften und Programmbibliotheken</h2>
      <p>Schriftarten und JavaScript-Bibliotheken werden ausschließlich von dieser Website selbst ausgeliefert. Es findet keine Verbindung zu Google Fonts oder zu einem externen CDN statt; Ihre IP-Adresse wird dafür an keinen Dritten übertragen. Bilder werden ebenfalls nur von dieser Website geladen.</p>

      <h2>4. KI-Assistent</h2>
      <p>Auf der Startseite können Sie Fragen an einen KI-Assistenten stellen. Wenn Sie eine Nachricht absenden, wird Folgendes verarbeitet:</p>
      <dl>
        <dt>Daten</dt><dd>Ihr Nachrichtentext, eine zufällige Gesprächskennung, die gewählte Sprache der Seite, Zeitpunkt der Anfrage</dd>
        <dt>Empfänger</dt><dd>Railway Corp., USA (Hosting des Workflows, der den Assistenten betreibt) und Anthropic, PBC, USA (Sprachmodell Claude, das die Antwort erzeugt)</dd>
        <dt>Zweck</dt><dd>Beantwortung Ihrer Frage im laufenden Gespräch; Schutz vor Missbrauch (Begrenzung der Anzahl von Fragen)</dd>
        <dt>Rechtsgrundlage</dt><dd>Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse, Fragen zu meinem beruflichen Profil zu beantworten); mit dem Absenden willigen Sie zugleich in die Verarbeitung Ihrer Eingabe ein (Art. 6 Abs. 1 lit. a DSGVO)</dd>
        <dt>Speicherdauer</dt><dd>Protokolle des Workflows (Frage und Antwort) werden nach höchstens 14 Tagen automatisch gelöscht. Anthropic nutzt Eingaben und Antworten der API nicht zum Training seiner Modelle und löscht sie nach eigenen Angaben innerhalb von 30 Tagen.</dd>
        <dt>Drittland</dt><dd>Beide Empfänger sitzen in den USA. Railway ist nach dem EU-U.S. Data Privacy Framework zertifiziert; die Übermittlung an Anthropic stützt sich auf die EU-Standardvertragsklauseln (Art. 46 Abs. 2 lit. c DSGVO), die Teil des Data Processing Addendum von Anthropic sind.</dd>
      </dl>
      <p>Die Nutzung des Assistenten ist freiwillig. Bitte geben Sie keine Gesundheitsdaten, Zugangsdaten oder andere besonders sensiblen Angaben ein und keine personenbezogenen Daten Dritter (etwa Namen und Kontaktdaten aus einer Stellenanzeige): dem Assistenten genügen die Anforderungen.</p>

      <h2>5. Speicherung im Browser</h2>
      <p>Damit die Nachrichten eines Gesprächs zusammengehalten werden, legt die Seite eine zufällige Kennung im Sitzungsspeicher (sessionStorage) Ihres Browsers ab; sie wird beim Schließen des Tabs gelöscht. Ihre Sprachwahl wird im lokalen Speicher (localStorage) des Browsers gemerkt. Beides ist technisch erforderlich im Sinne von § 25 Abs. 2 TDDDG und enthält keine personenbezogenen Angaben. Cookies werden nicht gesetzt; eine Webanalyse oder Werbung findet nicht statt.</p>

      <h2>6. Links zu anderen Diensten</h2>
      <p>Die Seite verlinkt auf LinkedIn, Telegram und GitHub. Erst wenn Sie einen Link anklicken, verlassen Sie diese Website; dort gelten die Datenschutzhinweise des jeweiligen Anbieters.</p>

      <h2>7. Ihre Rechte</h2>
      <p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) sowie das Recht, der Verarbeitung zu widersprechen (Art. 21). Eine erteilte Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen. Wenden Sie sich dafür an die oben genannte E-Mail-Adresse.</p>

      <h2>8. Beschwerderecht</h2>
      <p>Sie können sich bei einer Datenschutz-Aufsichtsbehörde beschweren. Für mich zuständig ist das Bayerische Landesamt für Datenschutzaufsicht (BayLDA), Promenade 18, 91522 Ansbach.</p>
    </section>
"""

privacy_en = f"""
    <section id="en" lang="en">
      <h1>Privacy policy</h1>
      <p class="stand">Last updated: {STAND}. The German version above is the authoritative one; this is a summary.</p>

      <h2>Controller</h2>
      <p><address>Vildana Razumova, {fill(ADDRESS_EN)}<br>E-mail: <a href="mailto:{EMAIL}">{EMAIL}</a></address></p>

      <h2>Hosting</h2>
      <p>The site is hosted on GitHub Pages (GitHub, Inc., USA). GitHub processes connection data such as your IP address, time of access and browser type to deliver the page (Art. 6(1)(f) GDPR). GitHub is certified under the EU-U.S. Data Privacy Framework.</p>

      <h2>Fonts, scripts, images</h2>
      <p>Everything is served from this site. Nothing is loaded from Google Fonts or any CDN.</p>

      <h2>The AI assistant</h2>
      <p>When you send a message, its text, a random conversation id, the page language and the time of the request go to my own workflow hosted at Railway (USA) and from there to Anthropic's Claude API (USA), which generates the answer. The purpose is to answer your question and to limit abuse (number of questions per conversation and per day). Workflow logs (question and answer) are deleted automatically after at most 14 days; Anthropic states that API inputs and outputs are not used to train its models and are deleted within 30 days. Railway is certified under the EU-U.S. Data Privacy Framework; transfers to Anthropic rely on the EU standard contractual clauses that are part of Anthropic's Data Processing Addendum.</p>
      <p>Using the assistant is voluntary. Please do not enter health data, credentials or other sensitive information, and no personal data of other people (for example names and contact details from a job posting): the requirements are enough.</p>

      <h2>Browser storage</h2>
      <p>A random conversation id is kept in your browser's sessionStorage (deleted when the tab closes) and your language choice in localStorage. Both are technically necessary and contain no personal data. No cookies, no analytics, no advertising.</p>

      <h2>Your rights</h2>
      <p>You may request access, rectification, erasure, restriction or portability of your data, object to processing and withdraw consent by writing to the e-mail address above. You may also complain to the Bavarian Data Protection Authority (BayLDA), Promenade 18, 91522 Ansbach, Germany.</p>
    </section>
"""

privacy_ru = f"""
    <section id="ru" lang="ru">
      <h1>Политика конфиденциальности</h1>
      <p class="stand">Обновлено: {STAND}. Юридически значима немецкая версия выше; это краткое изложение.</p>

      <h2>Ответственная за обработку</h2>
      <p><address>Вильдана Разумова (Vildana Razumova), {fill(ADDRESS_RU)}<br>E-mail: <a href="mailto:{EMAIL}">{EMAIL}</a></address></p>

      <h2>Хостинг</h2>
      <p>Сайт размещён на GitHub Pages (GitHub, Inc., США). GitHub обрабатывает технические данные подключения (IP-адрес, время запроса, тип браузера), чтобы отдать страницу (ст. 6(1)(f) GDPR). GitHub сертифицирован по EU-U.S. Data Privacy Framework.</p>

      <h2>Шрифты, скрипты, изображения</h2>
      <p>Всё загружается с этого сайта. Ничего не запрашивается у Google Fonts или внешних CDN.</p>

      <h2>ИИ-ассистент</h2>
      <p>Когда вы отправляете сообщение, его текст, случайный идентификатор разговора, выбранный язык страницы и время запроса уходят в мой workflow на хостинге Railway (США), а оттуда в Claude API компании Anthropic (США), которая формирует ответ. Цель: ответить на ваш вопрос и ограничить злоупотребления (число вопросов на разговор и в день). Журналы workflow (вопрос и ответ) автоматически удаляются не позднее чем через 14 дней; по заявлению Anthropic, входные данные и ответы API не используются для обучения моделей и удаляются в течение 30 дней. Railway сертифицирован по EU-U.S. Data Privacy Framework; передача данных Anthropic опирается на стандартные договорные условия ЕС, входящие в Data Processing Addendum компании Anthropic.</p>
      <p>Использование ассистента добровольно. Пожалуйста, не вводите данные о здоровье, пароли и другую чувствительную информацию, а также персональные данные других людей (например, имена и контакты из вакансии): достаточно требований.</p>

      <h2>Хранение в браузере</h2>
      <p>Случайный идентификатор разговора хранится в sessionStorage вашего браузера (удаляется при закрытии вкладки), выбранный язык — в localStorage. Оба технически необходимы и не содержат персональных данных. Без cookies, аналитики и рекламы.</p>

      <h2>Ваши права</h2>
      <p>Вы можете запросить доступ к своим данным, их исправление, удаление, ограничение обработки или перенос, возразить против обработки и отозвать согласие, написав на указанный выше e-mail. Жалобу можно подать в надзорный орган Баварии (BayLDA), Promenade 18, 91522 Ansbach, Германия.</p>
    </section>
"""

# ───────────────────────────── Impressum ─────────────────────────────
VAT_CHOICE = "[Umsatzsteuer: eine Zeile behalten — «Kleinunternehmerin im Sinne von § 19 UStG; eine Umsatzsteuer-Identifikationsnummer liegt nicht vor.» oder «Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: DE…» — oder den Absatz löschen]"

impressum_de = f"""
    <section id="de" lang="de">
      <h1>Impressum</h1>
      <p class="stand">Angaben gemäß § 5 DDG</p>

      <h2>Diensteanbieterin</h2>
      <p><address>Vildana Razumova<br>{fill(ADDRESS_DE)}</address></p>

      <h2>Kontakt</h2>
      <p>E-Mail: <a href="mailto:{EMAIL}">{EMAIL}</a><br>Weitere Kontaktwege: <a href="https://www.linkedin.com/in/vildanarazumova/" rel="noopener">LinkedIn</a>, <a href="https://t.me/vildanaraz" rel="noopener">Telegram</a></p>

      <h2>Umsatzsteuer</h2>
      <p>{fill(VAT_CHOICE)}</p>

      <h2>Verantwortlich für den Inhalt</h2>
      <p>Vildana Razumova, Anschrift wie oben.</p>

      <h2>Hinweis zum KI-Assistenten</h2>
      <p>Die Antworten des auf dieser Website eingebundenen Assistenten werden automatisiert durch ein Sprachmodell erzeugt. Sie beruhen auf einem von mir gepflegten Profil, können dennoch unvollständig oder fehlerhaft sein und stellen keine rechtlich verbindliche Auskunft dar. Bitte klären Sie wichtige Details direkt mit mir.</p>

      <h2>Streitbeilegung</h2>
      <p>Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>

      <h2>Urheberrecht</h2>
      <p>Der Quellcode dieser Website steht unter der MIT-Lizenz auf <a href="https://github.com/VildanaRazumova/about-me" rel="noopener">GitHub</a>. Texte, Profilinhalte und das Foto: © Vildana Razumova. Eingebundene Bibliotheken: marked (MIT) und DOMPurify (Apache-2.0 / MPL-2.0); Schriften Inter und Source Serif 4 (SIL Open Font License).</p>
    </section>
"""

impressum_en = f"""
    <section id="en" lang="en">
      <h1>Legal notice</h1>
      <p class="stand">Information required by § 5 of the German Digital Services Act (DDG). The German version is authoritative.</p>
      <p><address>Site owner: Vildana Razumova<br>{fill(ADDRESS_EN)}<br>E-mail: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="https://www.linkedin.com/in/vildanarazumova/" rel="noopener">LinkedIn</a> · <a href="https://t.me/vildanaraz" rel="noopener">Telegram</a></address></p>
      <p>Responsible for the content: Vildana Razumova, address as above. Answers produced by the assistant on this site are generated automatically by a language model from a profile I maintain; they may be incomplete or wrong and are not legally binding information. Source code: MIT licence on <a href="https://github.com/VildanaRazumova/about-me" rel="noopener">GitHub</a>; texts, profile content and photo © Vildana Razumova.</p>
    </section>
"""

impressum_ru = f"""
    <section id="ru" lang="ru">
      <h1>Выходные данные</h1>
      <p class="stand">Сведения по § 5 немецкого закона о цифровых услугах (DDG). Юридически значима немецкая версия.</p>
      <p><address>Владелица сайта: Вильдана Разумова (Vildana Razumova)<br>{fill(ADDRESS_RU)}<br>E-mail: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="https://www.linkedin.com/in/vildanarazumova/" rel="noopener">LinkedIn</a> · <a href="https://t.me/vildanaraz" rel="noopener">Telegram</a></address></p>
      <p>Ответственная за содержание: Вильдана Разумова, адрес выше. Ответы ассистента на этом сайте формируются языковой моделью автоматически на основе профиля, который я веду; они могут быть неполными или ошибочными и не являются юридически значимой информацией. Исходный код: лицензия MIT на <a href="https://github.com/VildanaRazumova/about-me" rel="noopener">GitHub</a>; тексты, содержание профиля и фото © Вильдана Разумова.</p>
    </section>
"""

(SITE / "privacy.html").write_text(page("Datenschutzerklärung", privacy_de + privacy_en + privacy_ru, "← Zurück / Back / Назад"), encoding="utf-8")
if WITH_IMPRESSUM:
    (SITE / "impressum.html").write_text(page("Impressum", impressum_de + impressum_en + impressum_ru, "← Zurück / Back / Назад"), encoding="utf-8")
for f in ("privacy.html",) + (("impressum.html",) if WITH_IMPRESSUM else ()):
    t = (SITE / f).read_text(encoding="utf-8")
    print(f, len(t), "bytes;", "placeholders:", t.count('class="fill"'))
