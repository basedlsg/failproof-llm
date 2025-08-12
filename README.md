# Failproof-LLM

[![CI](https://github.com/failproof-llm/failproof-llm/actions/workflows/ci.yml/badge.svg)](https://github.com/failproof-llm/failproof-llm/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/failproof-llm/failproof-llm)](https://github.com/failproof-llm/failproof-llm/releases/latest)
[![License](https://img.shields.io/github/license/failproof-llm/failproof-llm)](LICENSE)

## Mission

To create a comprehensive, open-source framework for evaluating the robustness and safety of Large Language Models (LLMs) against common failure modes.

## Quickstart

This project uses `make` to streamline setup and execution.

### Setup

To install all dependencies and set up the environment, run:

```bash
make setup
```

### Run the Demo

To run the interactive demo, which showcases the dashboard and API, use:

```bash
make demo
```

### Development

To start the development server, which includes hot-reloading for both the backend and frontend, run:

```bash
make dev
```

## Dashboard Preview

Here's a sneak peek of the dashboard:

![Dashboard Screenshot](https://user-images.githubusercontent.com/12345/67890.png)

## Project Structure

The project is organized into the following main directories:

*   `backend`: Contains all the core logic for the framework, including test execution, scoring, and API integrations.
*   `web`: Includes the frontend components and pages for the web-based user interface.
*   `suites`: Houses the various test suites for evaluating LLMs.
*   `reports`: Stores the output and templates for the evaluation reports.
*   `docs`: Contains the project documentation.
## Quickstart (v0.1.0)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/failproof-llm/failproof-llm.git --branch v0.1.0
    cd failproof-llm
    ```

2.  **Set up the environment:**
    ```bash
    make setup
    ```

3.  **Run the demo:**
    ```bash
    make demo
    ```

4.  **Start the development servers:**
    ```bash
    make dev
    ```

5.  **View the results:**
    *   API: `http://127.0.0.1:8000`
    *   Dashboard: `http://127.0.0.1:3000`

## Screenshots

**Run List**

![Run List](placeholder.png)

**Case Detail**

![Case Detail](placeholder.png)

## Common Errors

| Error | Cause | Solution |
| --- | --- | --- |
| Missing API Key | The `OPENAI_API_KEY` environment variable is not set. | Set the `OPENAI_API_KEY` in a `.env` file. |
| 403 CORS | The request is coming from an origin that is not allowed. | Add the origin to the `ALLOWED_ORIGINS` environment variable. |
| Port in use | Another process is using port 8000 or 3000. | Stop the other process or change the port in the `Makefile`. |