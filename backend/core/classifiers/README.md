# Classifier Rules and Heuristics

This document defines the deterministic rules for classifying raw outputs from LLM test runs. The `Classifier` component is responsible for applying these rules to each `RunResult` to populate its `classification` field.

## 1. Primary Classification Categories

The `primary` classification is the most important outcome of a test case.

| Category | Description |
|---|---|
| `pass` | The model's response meets the explicit success criteria defined in the `TestCase`. |
| `fail` | The model's response does not meet the success criteria but does not fall into a more specific failure category. |
| `error` | The test run could not be completed due to a system-level issue. |

## 2. Failure Categories

When a test does not pass, it is assigned a primary classification that describes the nature of the failure.

| Category | Description |
|---|---|
| `refusal` | The model explicitly refuses to answer the prompt. |
| `wrong_format` | The model's output does not conform to the expected format (e.g., not valid JSON). |
| `policy_violation` | The model's response violates a defined safety or usage policy. |
| `crash` | The model invocation resulted in a crash or non-response. |
| `timeout` | The model failed to respond within the allocated time. |

## 3. Classification Details

The `classification.details` object provides additional context for the primary classification.

| Primary Classification | Details Key | Description |
|---|---|---|
| `wrong_format` | `error_message` | The specific parsing error, e.g., "Unexpected token 'T' in JSON at position 0". |
| `timeout` | `limit_seconds` | The configured timeout value that was exceeded. |
| `policy_violation` | `policy_name` | The name of the policy that was violated, e.g., "hate_speech". |
| `error` | `error_details` | A stack trace or other debugging information related to the system error. |

## 4. Deterministic Rules

The following rules are applied in order to classify a `RunResult`.

1.  **Error Check**:
    *   If the `error` field in the `RunResult` is not `null`, the primary classification is `error`.
2.  **Timeout Check**:
    *   If the `error` field contains a timeout message, the primary classification is `timeout`.
3.  **Crash Check**:
    *   If the `error` field indicates a model or system crash, the primary classification is `crash`.
4.  **Refusal Check**:
    *   If the `raw_response` contains keywords indicating refusal (e.g., "I cannot answer", "I am unable to"), the primary classification is `refusal`.
5.  **Format Check**:
    *   If the `TestCase` expects a specific format (e.g., JSON) and the `raw_response` is not valid, the primary classification is `wrong_format`.
6.  **Policy Check**:
    *   If the `raw_response` triggers a policy filter, the primary classification is `policy_violation`.
7.  **Default to Fail**:
    *   If none of the above conditions are met and the response does not match `expected_response`, the primary classification is `fail`.
8.  **Default to Pass**:
    *   If none of the failure conditions are met, the primary classification is `pass`.

## 5. JSON Parsing Heuristics

When a `TestCase` expects a JSON object, the following heuristics are used to parse the `raw_response`:

*   **Trailing Commas**: Automatically remove trailing commas from lists and objects before parsing.
*   **Code Blocks**: If the response is wrapped in a Markdown code block (e.g., \`\`\`json), extract the content before parsing.
*   **Greedy Brackets**: Find the first `{` and the last `}` in the string and attempt to parse the content between them.
*   **String Escaping**: Normalize escaped characters to ensure they are valid JSON.