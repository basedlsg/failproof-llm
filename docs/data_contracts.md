# FailProof LLM: Data Contracts

This document provides the canonical definition for all data structures and interfaces used within the FailProof LLM system. These contracts are the single source of truth and must be adhered to by all components.

## 1. TestCase Schema

A `TestCase` represents a single, executable test unit. It contains all the information needed for the `Runner` to invoke a model and for the `Classifier` to evaluate the result.

**Location**: Defined in `suites/**/*.jsonl`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TestCase",
  "description": "A single test case for an LLM.",
  "type": "object",
  "properties": {
    "case_id": {
      "description": "A unique identifier for the test case, e.g., 'injection-001'.",
      "type": "string"
    },
    "suite_id": {
      "description": "The ID of the test suite this case belongs to, e.g., 'injection'.",
      "type": "string"
    },
    "prompt": {
      "description": "The exact text to be sent to the LLM.",
      "type": "string"
    },
    "prompt_vars": {
      "description": "A dictionary of variables to be interpolated into the prompt string.",
      "type": "object",
      "additionalProperties": {
        "type": "string"
      }
    },
    "expected_response": {
      "description": "A description or pattern of the expected response. Can be a regex or a simple string.",
      "type": "string"
    },
    "expected_classification": {
      "description": "The primary classification expected for this test case if it behaves correctly.",
      "type": "string",
      "enum": ["pass", "fail"]
    },
    "tags": {
      "description": "A list of tags for categorization and filtering.",
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "case_id",
    "suite_id",
    "prompt"
  ]
}
```

## 2. RunResult Schema

A `RunResult` is the output of a single `TestCase` execution. It is stored as a single line in a run-specific JSONL file. The object is built progressively: the `Runner` creates the initial object, the `Classifier` adds the `classification` field, and the `Scorer` adds the `scores` field.

**Location**: Stored in the `run_results` table in the SQLite database. Managed by the `StorageManager`.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RunResult",
  "description": "The result of a single TestCase execution against a model.",
  "type": "object",
  "properties": {
    "case_id": {
      "description": "The ID of the TestCase that was run.",
      "type": "string"
    },
    "suite_id": {
      "description": "The ID of the test suite.",
      "type": "string"
    },
    "run_id": {
      "description": "A unique identifier for the entire test run.",
      "type": "string"
    },
    "model_id": {
      "description": "The identifier of the model that was tested, e.g., 'gpt-4-turbo'.",
      "type": "string"
    },
    "timestamp_utc": {
      "description": "The ISO 8601 timestamp of when the test was executed.",
      "type": "string",
      "format": "date-time"
    },
    "raw_response": {
      "description": "The complete, unmodified response from the LLM.",
      "type": "string"
    },
    "error": {
      "description": "Any error message captured during the run. Null if successful.",
      "type": ["string", "null"]
    },
    "classification": {
      "description": "The deterministic classification assigned by the Classifier.",
      "type": "object",
      "properties": {
        "primary": {
          "description": "The main classification, e.g., 'pass', 'fail', 'refusal'.",
          "type": "string"
        },
        "details": {
          "description": "Additional details or secondary classifications.",
          "type": "object"
        }
      },
      "required": ["primary"]
    },
    "scores": {
      "description": "Quantitative scores assigned by the Scorer.",
      "type": "object",
      "properties": {
        "accuracy": {
          "description": "Binary score: 1 for a pass, 0 for a fail.",
          "type": "number",
          "enum": [0, 1]
        }
      },
      "required": ["accuracy"]
    }
  },
  "required": [
    "case_id",
    "suite_id",
    "run_id",
    "model_id",
    "timestamp_utc"
  ]
}
```

## 3. ModelClient Interface

The `ModelClient` provides a consistent, technology-agnostic interface for interacting with various LLM providers. All model adapters must implement this interface.

This will be defined as a Python `Protocol` to allow for structural subtyping (duck typing), which gives us flexibility in implementation.

```python
# Location: backend/adapters/model_client.py
from typing import Protocol, Dict, Any

class ModelClient(Protocol):
    """
    An interface for a client that communicates with a Large Language Model.
    """

    def __init__(self, api_key: str, model_id: str):
        """
        Initializes the client with necessary credentials and model information.

        Args:
            api_key: The API key for the LLM provider.
            model_id: The specific model to be used (e.g., 'gpt-4-turbo').
        """
        ...

    def get_completion(self, prompt: str, params: Dict[str, Any]) -> str:
        """
        Gets a completion from the LLM for a given prompt.

        Args:
            prompt: The prompt to send to the model.
            params: A dictionary of provider-specific parameters 
                    (e.g., temperature, max_tokens).

        Returns:
            The model's response as a string.

        Raises:
            Exception: If the API call fails for any reason.
        """
        ...
