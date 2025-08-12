# Contradictions Test Suite

**Suite ID:** `contradictions`

## Description

This suite tests the model's ability to identify and avoid self-contradictions within a single response. The test cases are designed to elicit responses where the model might state a fact and then later contradict it, or provide logically inconsistent information.

## Failure Types

This suite is designed to catch the following failure types:

*   **`logical-fallacy`**: The model's response contains a logical fallacy (e.g., circular reasoning).
*   **`self-contradiction`**: The model makes a statement that directly contradicts another statement in the same response.
*   **`factual-inconsistency`**: The model presents facts that are inconsistent with each other.