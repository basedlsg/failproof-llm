# JSON API Test Suite

**Suite ID:** `json_api`

## Description

This suite tests the model's ability to generate well-formed JSON that conforms to a specified schema. It includes prompts that ask the model to produce JSON output for various scenarios, such as generating API responses, configuration files, or structured data.

## Failure Types

This suite is designed to catch the following failure types:

*   **`format-error`**: The model produces output that is not valid JSON (e.g., missing commas, incorrect quoting).
*   **`schema-violation`**: The model produces valid JSON, but it does not conform to the requested schema (e.g., missing required fields, incorrect data types).
*   **`incomplete-json`**: The model's output is truncated, resulting in incomplete JSON.