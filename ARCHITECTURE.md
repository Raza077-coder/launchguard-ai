# LaunchGuard AI

## Repository overview

This repository contains a modular MVP for LaunchGuard AI built as a monorepo with a FastAPI backend and a Next.js frontend. The implementation intentionally prioritizes deterministic, evidence-backed scanning and a secure local-first workflow over fabricated metrics or simulated completion states.

## Phase status

### Phase 1 — Complete scaffold
- Backend package structure created.
- FastAPI application with health and project endpoints.
- SQLite database layer and domain models.
- URL validation and SSRF protections.
- Deterministic scanner job layer.
- Fixture website and baseline tests.

### Phase 2 — Frontend scaffold
- Next.js + TypeScript + Tailwind project scaffold.
- Landing page and dashboard screens.
- Scan wizard and report page placeholders connected to the API layer.

### Phase 3 — remaining work
- Full browser scan workflow over fixture pages.
- AI diagnosis and repair-planning integration.
- Full verification runner and approval flow.
- Production-quality report UX and analytics.

## Core structure

- `backend/` – FastAPI app, SQLite models, scanner, tests
- `frontend/` – Next.js app
- `docs/` – API, setup, architecture, and security docs
- `fixtures/` – local static test site
