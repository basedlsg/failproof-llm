# Test Suites

This document outlines the test suites used in the FailProof LLM project. Each suite is designed to target a specific category of potential failures in Large Language Models.

## Coverage Matrix

The following table provides an overview of the test suites and the types of failures they are designed to catch.

| Suite ID | Description | Failure Types Covered |
| :--- | :--- | :--- |
| `json_api` | Tests the model's ability to generate well-formed JSON that conforms to a specified schema. | `format-error`, `schema-violation`, `incomplete-json` |
| `injection` | Tests the model's vulnerability to prompt injection attacks. | `prompt-injection`, `instruction-hijack`, `privilege-escalation` |
| `long_context` | Tests the model's ability to maintain context and recall information over long conversations. | `context-loss`, `recency-bias`, `information-omission` |
| `unicode_locale` | Tests the model's handling of non-ASCII characters, different locales, and unicode standards. | `encoding-error`, `locale-misinterpretation`, `mojibake` |
| `contradictions` | Tests the model's ability to identify and avoid self-contradictions within a single response. | `logical-fallacy`, `self-contradiction`, `factual-inconsistency` |
