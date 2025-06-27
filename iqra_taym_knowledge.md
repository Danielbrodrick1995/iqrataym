## Iqra Taym – Islamic Knowledge Oracle

### Product Vision
Iqra Taym is a source-anchored Islamic AI assistant that mirrors the fast, minimal UX of Perplexity while ensuring every answer is grounded in authentic Islamic sources (Qur'an, Sahih Hadith, classical scholarship, and recognised fiqh opinions).

### Core Principles
1. Truth-Centric: Report only what is supported by authentic sources.
2. Bias Deconstruction: Recognise modern/personal bias and respond with evidence-based clarifications.
3. Non-Fluctuating: Maintain consistent rulings in line with traditional knowledge.
4. Source-First Responses: Cite references explicitly (e.g. "📖 Qur'an 2:2", "Sahih Muslim 234").
5. Modern UX: Clean, mobile-first chat interface inspired by Perplexity.

### Phase 1 – Foundation (This repository)
- [ ] ❶ Run existing Farfalle front-/back-end locally with our OpenAI key.
    • Configure `.env` with `OPENAI_API_KEY` and `NEXT_PUBLIC_API_URL`.
    • `docker compose -f docker-compose.dev.yaml up --build`.
- [ ] ❷ Smoke-test chat flow using `GPT-4o-mini` model.
- [ ] ❸ Document local dev workflow (pnpm / poetry).

### Phase 2 – Rebrand to Iqra Taym
- [ ] Replace logos and colour palette (green / gold theme).
- [ ] Update titles, meta tags, and favicon.
- [ ] Update copy in UI components (e.g. starter questions).

### Phase 3 – Islamic Knowledge Integration
- [ ] Curate structured database of Qur'an, Hadith collections, Tafsir & fiqh texts.
- [ ] Implement retrieval-augmented generation (RAG) pipeline that always injects source passages.
- [ ] Support multi-madhhab opinions where applicable.

### Phase 4 – Bias Resistance & Validation
- [ ] Add guardrails / prompting strategy to detect unsupported claims.
- [ ] Automated unit tests validating citation correctness.

### Phase 5 – Production Deployment
- [ ] Deploy on Render / Fly.io or similar.
- [ ] CI/CD workflow with GitHub Actions.
- [ ] Privacy & terms pages.

---
_Last updated: {{DATE}}_ 