# Unicode & Locale Test Suite

**Suite ID:** `unicode_locale`

## Description

This suite tests the model's ability to handle non-ASCII characters, different locales, and Unicode standards correctly. The test cases include prompts with various languages, scripts, and symbols to ensure the model can process and generate them without errors.

## Failure Types

This suite is designed to catch the following failure types:

*   **`encoding-error`**: The model produces garbled or incorrect characters (mojibake) due to encoding issues.
*   **`locale-misinterpretation`**: The model misinterprets cultural or linguistic nuances, such as date formats, number formats, or collation.
*   **`mojibake`**: The model produces unintelligible characters due to text encoding/decoding issues.