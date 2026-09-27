# Don't read my CV. Ask it.

A personal AI assistant that answers recruiters' questions about my work in English, German or Russian. Live at **https://vildanarazumova.github.io/about-me/**.

This repository holds only the page (`docs/`, served by GitHub Pages). The knowledge base, the assistant's rules and the workflow are private.

## How it is built

- **Page**: one static HTML/JS file, no frameworks, no build step, no analytics. It sends the question to the workflow and renders the answer. Fonts and the two libraries it uses (marked, DOMPurify) are bundled in the page, so nothing is loaded from third parties.
- **Workflow**: n8n on Railway. It detects the reply language in code, applies usage limits (per conversation and per day), adds the knowledge base and the rules to the prompt and calls Claude (Anthropic).
- **Knowledge**: Markdown and YAML files I write and maintain myself (facts, project cards, interview stories), assembled into one text by build scripts. No vector database: the whole profile fits into the prompt.
- **Principles**: honesty over persuasion (no superlatives, no invented experience, "I don't know" when the knowledge base is silent); employer projects at use-case level; public and private knowledge in separate folders; the assistant has no tools and can only read the text it is given.

Ask the assistant itself how it is built; it can explain the design.

## Rights

Page code (`docs/index.html`, `docs/privacy.html`): © Vildana Razumova. Bundled libraries: [marked](https://github.com/markedjs/marked) (MIT) and [DOMPurify](https://github.com/cure53/DOMPurify) (Apache-2.0 / MPL-2.0). Fonts Inter and Source Serif 4 (SIL Open Font License, see `docs/fonts/LICENSE.txt`). Content and photo: all rights reserved.
