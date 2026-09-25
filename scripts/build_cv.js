// CV, Vildana Razumova, in her own layout (Roboto / Roboto Light, centered header, grey right-aligned dates,
// sections with a thin rule, dash bullets). Public version: email and city, no phone, no street address.
// Facts come from second-brain/public/facts.yaml and the project cards; employer projects at use-case level,
// with the products she used (Dify, Microsoft Teams, Jira, SharePoint, Airflow, n8n, PostgreSQL) named as in the cards.
// ATS-friendly on purpose: one column, no tables or text boxes, no headers/footers, standard section names,
// dates as "Month YYYY - Month YYYY", plain hyphens, no special dashes or curly quotes.
//
// Build:  node scripts/build_cv.js CV_Vildana_Razumova.docx
// PDF:    soffice --headless --convert-to pdf CV_Vildana_Razumova.docx   (Roboto must be installed)
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, ExternalHyperlink, AlignmentType, LevelFormat, TabStopType, BorderStyle, Tab,
} = require("docx");

const R = "Roboto", RL = "Roboto Light";
const DARK = "303030", GREY = "999999", BLACK = "000000";
const PAGE_W = 12240, PAGE_H = 15840, M_LEFT = 675, M_RIGHT = 720, M_TB = 720;
const RIGHT_TAB = PAGE_W - M_LEFT - M_RIGHT; // 10845

const t = (text, o = {}) => new TextRun({ text, font: o.font || RL, size: o.size || 20, bold: o.bold, color: o.color || DARK });
const link = (text, url, o = {}) => new ExternalHyperlink({
  link: url,
  children: [new TextRun({ text, font: o.font || RL, size: o.size || 20, color: o.color || DARK, underline: {} })],
});
const tab = () => new TextRun({ children: [new Tab()] });
const P = (children, o = {}) => new Paragraph({
  children,
  alignment: o.align,
  spacing: { before: o.before ?? 0, after: o.after ?? 40, line: o.line || 264 },
  tabStops: o.tabs ? [{ type: TabStopType.RIGHT, position: RIGHT_TAB }] : undefined,
  keepNext: o.keepNext,
});

const center = (children, o = {}) => P(children, { ...o, align: AlignmentType.CENTER });
const section = (title) => new Paragraph({
  children: [t(title, { font: R, size: 26, color: BLACK })],
  spacing: { before: 200, after: 80 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BLACK, space: 1 } },
  keepNext: true,
});
const company = (name, descr, location) => P(
  [t(name + ":", { font: R, size: 21 }), t(" " + descr, { color: GREY }), tab(), t(location, { color: GREY })],
  { before: 140, after: 0, tabs: true, keepNext: true },
);
const role = (title, dates) => P(
  [t(title, { font: R, size: 22 }), tab(), t(dates, { color: GREY })],
  { after: 20, tabs: true, keepNext: true },
);
const intro = (text) => P([t(text)], { align: AlignmentType.JUSTIFIED, after: 40, keepNext: true });
const B = (text) => new Paragraph({
  children: [t(text)],
  numbering: { reference: "dash", level: 0 },
  alignment: AlignmentType.JUSTIFIED,
  spacing: { after: 20, line: 264 },
});
const stack = (text) => P([t(text, { font: R, size: 19 })], { before: 40, after: 0 });
const twoLine = (left, right, leftGrey) => P(
  [t(left, { font: leftGrey ? RL : R, size: leftGrey ? 20 : 21, color: leftGrey ? GREY : DARK }), tab(), t(right, { color: GREY })],
  { after: leftGrey ? 40 : 0, tabs: true, keepNext: !leftGrey },
);
const certLine = (name, org, date) => P(
  [t(name, { font: R, size: 21 }), t(org ? "  " + org : "", { color: GREY }), tab(), t(date, { color: GREY })],
  { after: 30, tabs: true },
);
const kv = (k, v) => P([t(k + ": ", { font: R, size: 20 }), t(v)], { align: AlignmentType.JUSTIFIED, after: 40 });

const doc = new Document({
  creator: "Vildana Razumova",
  title: "CV Vildana Razumova",
  description: "Data Scientist | AI Automation Specialist",
  styles: { default: { document: { run: { font: RL, size: 20, color: DARK } } } },
  numbering: {
    config: [{
      reference: "dash",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "-", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 270, hanging: 180 } }, run: { font: RL, color: DARK } },
      }],
    }],
  },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: M_TB, right: M_RIGHT, bottom: M_TB, left: M_LEFT } } },
    children: [
      // Header
      center([t("Vildana Razumova", { font: R, size: 32, color: BLACK })], { after: 0 }),
      center([t("Data Scientist | AI Automation Specialist", { size: 26 })], { after: 60 }),
      center([
        link("wildanka1@gmail.com", "mailto:wildanka1@gmail.com"), t(" • "),
        link("LinkedIn", "https://www.linkedin.com/in/vildanarazumova/"), t(" • "),
        link("GitHub", "https://github.com/VildanaRazumova"), t(" • "),
        link("Telegram", "https://t.me/vildanaraz"), t(" • "),
        t("Ingolstadt, Germany • Work permit for Germany and the EU"),
      ], { after: 20 }),
      center([t("Ask my AI assistant about my work: "), link("vildanarazumova.github.io/about-me", "https://vildanarazumova.github.io/about-me/")], { after: 100 }),
      P([t(
        "Data Scientist and AI Automation Specialist with a 10-year background in banking analytics and risk management and 1.5 years " +
        "in e-commerce product delivery. Since October 2025 the only data scientist at a tour operator: price recommendations on LightGBM " +
        "and business rules, an LLM assistant on Dify in Microsoft Teams, REST API integrations and daily data pipelines in Airflow and n8n. " +
        "M.Sc. in Data Science, AI and Digital Business (thesis graded 96/100) and an MBA. Open to AI automation and AI or analytics product " +
        "roles in a team; on-site, hybrid or remote."
      )], { align: AlignmentType.JUSTIFIED, after: 40 }),

      // Experience
      section("Experience"),
      company("Fun&Sun", "a leading tour operator in Central Asia", "Remote from Germany"),
      role("Data Scientist / AI Automation Specialist (freelance)", "October 2025 - present"),
      intro("Lead of the ML pricing project and the only data scientist on the team. Replaced manual, spreadsheet-based work with data pipelines, ML models and LLM assistants."),
      B("Built price recommendations for package tours: a LightGBM demand forecast with time-series cross-validation, combined with business rules learned from managers' past decisions; every recommendation is explained in plain language. In pilot: managers decide, nothing changes automatically. Forecast error about a third lower than a naive baseline."),
      B("Designed and built competitor price monitoring: an integration with an external data API and a daily Airflow pipeline with completeness checks and monitoring. Replaced manual collection that took up most of the working day of the team responsible. In production, handed over to another team with a runbook."),
      B("Built an LLM assistant for payment status questions: analysed six months of staff requests, wrote the scenarios and built the assistant on Dify in Microsoft Teams, with permissions and automated quality checks; for problem cases it opens a Jira ticket routed to the right team. In production since July 2026."),
      B("Delivered a REST API integration with a state registration service in n8n and PostgreSQL (retries, duplicate protection, daily reconciliation) and the PostgreSQL data layer for a traveller document web service that a developer, an infrastructure engineer and I launched in two days. In production."),
      B("Set up an AI-assisted way of working: a knowledge base per project in SharePoint, AI reviewers with separate roles (Claude), tests and data checks before every production change, so quality and knowledge do not depend on one person. In daily use."),
      stack("Stack: Python · SQL · pandas · scikit-learn · LightGBM · PostgreSQL · Airflow · n8n · Dify · Claude API · Claude Code · FastAPI"),

      company("Linde GmbH", "Global AI & Digital team", "Pullach, Germany"),
      role("AI Project Manager (internship during the Master's)", "July 2025 - December 2025"),
      B("Built a Power Automate workflow for content approval and supported the launch of an internal AI podcast; built a learning progress dashboard and used it to improve communication for a learning path on the global learning platform."),
      B("Product work on internal AI tools: user interviews and feedback, a test concept and test runs, documentation, a prioritised feature list and an MVP roadmap for an internal generative AI agent."),
      B("Official internship reference with the top overall rating."),

      company("Self development", "relocation to Germany", "Ingolstadt, Germany"),
      role("Career break", "May 2023 - June 2024"),
      B("Moved from Kazakhstan to Germany. Passed the German B1 exam and completed a B2 course."),
      B("Admitted to the M.Sc. in Data Science, AI and Digital Business at GISMA University of Applied Sciences."),

      company("Choco Holding (Chocofamily)", "e-commerce group, #1 discount service in Kazakhstan", "Almaty, Kazakhstan"),
      role("Project Manager and Business Analyst", "September 2021 - May 2023"),
      intro("Coordinated two teams of 7 developers and QA engineers: one improving the website and mobile app, one automating internal business processes. Introduced Scrum in a team of 8."),
      B("Saved 350+ working hours per month for 50+ internal CRM users by optimising 10+ business processes."),
      B("Increased successful payments by 33% by fixing the payment method used by 73% of users; conversion to purchase +23% after UX changes on the main screen."),
      B("Reduced a backlog of 500 issues by 40% with prioritisation frameworks; tech debt down 60% and development speed +55% after introducing Scrum."),
      B("Managed requirements and their changes, wrote technical documentation with UML and BPMN, ran discovery phases and audits of existing solutions."),

      company("Halyk Bank", "the largest universal commercial bank in Kazakhstan", "Almaty, Kazakhstan"),
      intro("Three analytics roles in 10.5 years, all about optimising financial processes and automating business processes."),
      role("Senior Operational Risk Manager, Financial Risk and Portfolio Analysis", "October 2017 - December 2021"),
      B("Automated the loss event database (100K+ events), saving 1,040 working hours a year for 2 employees; automated management reports on profit and operational risk."),
      B("Investigated internal and external fraud in 50+ cases under the Basel principles; 10+ scenario analyses across 5+ divisions and 20 key risk indicators across 10 divisions."),
      B("Reviewed 100+ new products and processes to identify and reduce operational risks."),
      role("Financial Analyst, Retail Sales", "July 2014 - October 2017"),
      B("Reviewed the financial results of 22 branches and 3,000 sub-branches; automated 10+ reports on payment devices and branch efficiency, saving 3+ hours of manual work daily."),
      role("Financial Accounting Analyst, Accounting and Reporting", "June 2011 - June 2014"),
      B("Prepared 30+ monthly regulatory reports to the National Bank of Kazakhstan; automated 30+ reports via SAP integration (loans, deposits, cards), regulator fines down from 4 a year to 0."),

      // Certifications
      section("Certifications"),
      certLine("Statistics and A/B Testing", "Stepik", "October 2024"),
      certLine("SQL Level Up", "Stepik", "October 2024"),
      certLine("Business Analysis in IT (BPMN, UML)", "Aleksander Belin School of Business Analysis", "May 2022"),
      certLine("Fast Track to MVP: Lean Strategies for Product Innovation; Digital Enthusiast: New Product Development", "", ""),

      // Education
      section("Education"),
      twoLine("Master in Data Science, AI and Digital Business", "Berlin (Potsdam), Germany"),
      twoLine("GISMA University of Applied Sciences", "2024 - 2026", true),
      B("Thesis: Multi-Horizon Load Factor Forecasting for B2B Charter Flights: A Machine Learning Approach. Grade 96/100."),
      twoLine("Master of Business Administration (MBA, AMBA-accredited programme)", "Almaty, Kazakhstan"),
      twoLine("Almaty Management University (AlmaU)", "2018 - 2019", true),
      twoLine("Bachelor in Finance", "Almaty, Kazakhstan"),
      twoLine("International Academy of Business (now Almaty Management University)", "2007 - 2011", true),

      // Skills
      section("Hard & Soft Skills"),
      kv("Machine Learning", "Python, SQL, pandas, NumPy, scikit-learn, LightGBM, XGBoost, time-series forecasting and cross-validation, feature engineering, explainable AI (SHAP), model evaluation, NLP"),
      kv("LLM & AI Automation", "Claude API, Claude Code, Dify, n8n, LLM applications and evaluation, prompt engineering, AI agents, FastAPI, REST API integration, Power Automate"),
      kv("Data Engineering & BI", "PostgreSQL, ClickHouse, MSSQL, Airflow, Docker, data pipelines, data modelling, data-quality monitoring, Power BI, DAX, Microsoft Excel, SAP FI"),
      kv("Business & Product", "Business analysis (BPMN, UML), requirements management, Scrum, prioritisation (RICE, MoSCoW, ICE), Jira, Confluence, Miro, Figma, operational risk management, stakeholder management"),
      kv("Soft Skills", "Clear communication, analytical problem solving and risk assessment, structured work with stakeholders, adaptability and fast learning, ownership of results"),

      // Languages
      section("Languages"),
      P([t("English: professional working proficiency • German: B1 certified, B2 course completed • Russian: native")], { after: 0 }),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(process.argv[2] || "cv.docx", buf); console.log("written", buf.length); });
