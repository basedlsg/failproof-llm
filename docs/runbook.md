# Runbook

This document provides instructions for common operational tasks.

## Development

To run the backend API server locally, use the following command:

```bash
uvicorn backend.api.main:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

## Verification

To verify the API is running correctly, use the following smoke test script:

```bash
# API
curl -s localhost:8000/api/v1/runs | jq '..id'           # expect an ID
RUN=$(curl -s localhost:8000/api/v1/runs | jq -r '..id')
curl -s localhost:8000/api/v1/runs/$RUN | jq '.scores'
curl -s localhost:8000/api/v1/runs/$RUN/cases?limit=1 | jq '..id'
CASE=$(curl -s localhost:8000/api/v1/runs/$RUN/cases?limit=1 | jq -r '..id')
curl -s localhost:8000/api/v1/cases/$CASE | jq '.classification'
curl -s localhost:8000/api/v1/runs/$RUN/report.md | head -n 5

# Dashboard
# open http://localhost:3000/runs
```