# Injection Test Suite

**Suite ID:** `injection`

## Description

This suite tests the model's vulnerability to prompt injection attacks. The test cases include various methods of embedding malicious or unintended instructions within a prompt, aiming to hijack the model's behavior.

## Failure Types

This suite is designed to catch the following failure types:

*   **`prompt-injection`**: The model executes unintended instructions hidden within the prompt.
*   **`instruction-hijack`**: The model ignores its original instructions and follows new, injected ones.
*   **`privilege-escalation`**: The model attempts to perform actions that it should not have access to, based on injected prompts.