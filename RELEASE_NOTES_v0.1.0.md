# FailProof LLM v0.1.0 (2025-08-10)

## Highlights
- Read-only API (versioned at **/api/v1**) to list runs, inspect a run, view cases, and fetch Markdown reports.
- Read-only dashboard (Run list, Run summary, Case detail, Compare runs).
- One-click demo (`make demo`) that executes a tiny suite end-to-end and generates a shareable report.

## What’s inside
- **API**: pagination on list endpoints, uniform error envelope, CORS for http://localhost:3000, `/healthz`.
- **Dashboard**: typed API client generated from `openapi.json`, empty/error/loading states, a11y pass.
- **Docs/CI**: Quickstart, smoke test script, OpenAPI validation job, coverage and SBOM artifacts.

## Artifacts
- `openapi.json` — API contract (source of truth for generated clients)
- `2025-08-10-07-47-00.md` — sample run report
- `coverage-report.xml` — backend coverage
- `sbom.json` — software bill of materials
- `checksums.txt` — SHA-256 hashes for all attached artifacts

## Known limitations
- Dashboard is read-only and does not yet include all planned features.
- API has no authentication (planned for v0.1.x).

## Getting started
```bash
make setup
make demo     # generates a run + report
make dev      # starts API + dashboard -> http://localhost:3000
```

## Compatibility & Stability

* API is served under `/api/v1`. Minor `0.1.x` releases will be **additive** only.

## Acknowledgements

Thanks to the Committees (TestGen, Runner, Classifier, Scoring, UI, Reporting), CTO, and Head of Ops for specs, QA, and gating.