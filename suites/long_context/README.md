# Long Context Test Suite

**Suite ID:** `long_context`

## Description

This suite tests the model's ability to maintain context and recall information over long conversations or large amounts of text. The test cases involve providing the model with a significant amount of information and then asking questions that require recalling specific details from earlier in the context.

## Failure Types

This suite is designed to catch the following failure types:

*   **`context-loss`**: The model forgets information that was provided earlier in the conversation.
*   **`recency-bias`**: The model gives more weight to recent information and ignores or contradicts earlier information.
*   **`information-omission`**: The model fails to use all relevant information from the context to answer a question.