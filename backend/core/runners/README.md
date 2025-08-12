# Runners

This document outlines the design for the test suite runner, which is responsible for executing a suite of test cases against a model and recording the results.

## Run Loop Plan

The runner will execute test suites sequentially. The process is as follows:

1.  **Load Test Suite:** The runner loads a test suite from a `.jsonl` file (e.g., `suites/json_api/examples.jsonl`). Each line in the file represents a `TestCase` object.
2.  **Initialize Run:** A unique `run-id` is generated for the execution.
3.  **Iterate Test Cases:** The runner iterates through each `TestCase` in the suite.
4.  **Execute Test Case:** For each `TestCase`, the runner sends the `prompt` to the target model.
5.  **Record Result:** The model's response is captured as a `RunResult`, along with metadata such as the `run-id`, `timestamp`, and `execution_time`.
6.  **Store Artifacts:** The raw model output and any logs are stored in the artifacts directory.
7.  **Complete Run:** After all test cases are executed, the run is marked as complete.

## Timeout & Retry Policy

To handle unresponsive or slow models, the following policy will be implemented:

*   **Timeout:** Each request to the model will have a timeout of **30 seconds**.
*   **Retry Policy:** If a request times out or fails with a transient error, the runner will retry the request up to **3 times**.
*   **Backoff Strategy:** An exponential backoff strategy will be used between retries to avoid overwhelming the model. The delay will be calculated as `2^n` seconds, where `n` is the retry attempt number (e.g., 2s, 4s, 8s).

## Artifact Path Convention

The runner produces two types of outputs: the final `RunResult` file and supplementary artifacts.

### Primary Output: RunResult File

The primary output is a consolidated JSONL file containing a `RunResult` object for each test case in the run. As defined in the master data contract, this file must be written directly to the `reports/` directory.

*   **Path:** `reports/{run_id}.jsonl`
*   **`<run_id>`:** A unique identifier for the test run (e.g., a timestamp or a UUID).

### Supplementary Artifacts

All other artifacts for a given run, such as raw model logs or intermediate files, are stored in a dedicated subdirectory within `reports/`.

*   **Path:** `reports/artifacts/<run-id>/`

This directory may contain:
*   Raw model outputs for each test case.
*   Execution logs.
*   A summary report of the run.