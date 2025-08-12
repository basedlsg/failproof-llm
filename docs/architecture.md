# Architecture

This document provides an overview of the system architecture for the FailProof LLM project.

## API

The backend exposes a read-only RESTful API built with FastAPI.

### Endpoints

*   **`GET /api/runs`**: Retrieves a list of all test runs.
*   **`GET /api/runs/{id}`**: Retrieves detailed information for a single test run.
*   **`GET /api/runs/{id}/cases`**: Retrieves all test case results for a specific run.
*   **`GET /api/cases/{id}`**: Retrieves detailed information for a single test case result.
*   **`GET /api/runs/{id}/report.md`**: Retrieves the full Markdown report for a specific run.

### Authentication

The API is currently open and does not require authentication.

### Schema

The API schema is defined using the OpenAPI standard and is available at `/openapi.json`. The schema is also committed to the repository at `backend/api/openapi.json`.