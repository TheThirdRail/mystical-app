# MetaMystic – Product Requirements Document (PRD)  
**Version 1.0 | Owner:** John Titor  
**Last updated:** 28 May 2025

---

## 1 Product Vision
Deliver an AI-assisted, multi-discipline spiritual reading platform that partners (tarot readers, astrologers, numerologists) can embed on their own sites and promote via a white-label mobile app.  
The platform blends tropical & sidereal astrology, Chinese zodiac, numerology, and tarot into one cohesive reading. Each partner gets a custom “persona” (photo, bio, deck, rules, tone) so end-users feel they are interacting with that specific guide. Revenue from a reading is automatically tallied per partner for monthly payouts.

---

## 2 Target Users
| Persona | Description | Need |
|---------|-------------|------|
| **Curious Seeker** | 18-40, mobile-first, enjoys horoscopes & tarot memes | Quick, upbeat guidance; privacy; low price |
| **Partner Guide** | Practising spiritual coach with an online following | Seamless embed; custom deck/spreads; revenue share |
| **White-Label Consumer** | Visitor to a partner’s site or follower on social media | Same as Curious Seeker, but styled by that partner |

---

## 3 Success Metrics
* **Time-to-first-reading:** < 60 sec from landing page  
* **Reading completion rate:** > 80 %  
* **Partner monthly payout accuracy:** 100 %  
* **Average reading NPS:** ≥ 50  
* **Partner acquisition:** 10 active partners within 6 months  

---

## 4 Features

### 4.1 Core Reading Engine  
* Tropical & sidereal charts with selectable ayanamsa  
* Chinese zodiac animal calculation  
* Numerology core numbers  
* Tarot draws with upright/reversed orientation  
* Standard spreads: 1-Card, 3-Card, Celtic Cross, Horseshoe, etc.  
* AI narrative that merges all systems in a positive tone

### 4.2 Partner Persona System  
* Upload photo (JPG/PNG) and “about me” text  
* Optional prompt-stub to inflect AI voice (style, cadence)  
* Custom tarot decks (image set + JSON metadata)  
* Custom spreads (JSON layout)  
* Rule overrides (e.g., custom compatibility logic)

### 4.3 Multi-Provider LLM Support  
* Abstract `LLMProvider` (OpenAI, Anthropic, Google, Meta)  
* Runtime switch via env variable or admin UI

### 4.4 Admin & Reporting  
* Role-based auth: admin, partner  
* Dashboard: usage stats, reading logs, earnings per partner  
* CSV export for payouts

### 4.5 Mobile & Web Clients  
* Web: React SPA (partners can iframe or subdomain)  
* Mobile: React Native app (Expo) for iOS & Android  
* Offline cache of static assets (card images)

### 4.6 Internationalization (Phase 2)  
* Locale files for UI strings  
* Reading output auto-translated via LLM

### 4.7 Voice Interaction (Phase 3)  
* TTS playback of readings  
* Optional speech-to-text for questions

---

## 5 Technical Overview

| Layer | Choice | Reason |
|-------|--------|--------|
| **Backend** | FastAPI + PostgreSQL | Async speed, simple JSON API, low cost |
| **Astrology** | Kerykeion (Swiss Ephemeris) | High precision, sidereal toggle |
| **Chinese Zodiac** | Lightweight zodiac library | Minimal dependency |
| **Numerology** | numerology package | Covers core numbers, easy to extend |
| **Tarot** | Custom module + JSON deck | Maximum flexibility for custom decks |
| **Media Storage** | S3-compatible (R2/Backblaze) | Cheap, CDN ready |
| **Auth** | JWT | Works for web & mobile |
| **Mobile** | React Native (Expo) | Shared JS code, fast iteration |
| **Hosting (MVP)** | $5 VPS (Docker Compose) | Full control, upgrade later |
| **Scaling Path** | Managed Postgres + extra API pods | Linear cost growth |

---

## 6 User Flows

### New Reading (Web or Mobile)  
1. User selects partner (or default MetaMystic).  
2. Inputs birth data (+ optional question).  
3. App POSTs to `/reading/full`.  
4. Backend calls calculators → builds AI prompt → gets narrative.  
5. Response JSON rendered into UI with card images & results.

### Partner Sign-Up  
1. Partner registers account.  
2. Uploads photo, bio, deck images, deck.json, spreads.json.  
3. Tests readings in preview mode.  
4. Publishes embed code on their website.  
5. Earnings tracked automatically against partner_id.

---

## 7 Non-Functional Requirements
* **Positivity filter:** narrative must avoid fatalistic language.  
* **Privacy:** birth data encrypted in transit, no raw logs.  
* **Upright <-> reversed randomness:** cryptographically secure RNG.  
* **A11y:** WCAG AA on web, RN accessibility labels.  
* **Latency target:** < 3 s p95 for `/reading/full`.

---

## 8 Roadmap

| Quarter | Milestone |
|---------|-----------|
| **Q3 2025** | MVP web app + 1 native build; 2 pilot partners |
| **Q4 2025** | In-app purchases, multi-LLM switch, payout CSV |
| **Q1 2026** | Multilingual UI + auto translation |
| **Q2 2026** | Voice (TTS + STT), BaZi beta, desktop PWA |

---

## 9 Risks & Mitigations
* **LLM cost spikes** – Allow provider switch & prompt caching.  
* **Partner content abuse** – Validation pipeline & admin review.  
* **Regulatory (astrology disclaimers)** – Include “for entertainment only” footer in every reading.  
* **Mobile store policy changes** – Keep web app as fallback revenue channel.

---

## 10 Open Questions
1. Exact revenue-split contract terms with partners?  
2. Minimum viable content set for non-partner personas?  
3. Whether to auto-generate partner decks from template or require manual upload?  
4. Preferred in-app purchase processor (Stripe vs native stores)?

---