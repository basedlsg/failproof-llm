import pytest
from pydantic import ValidationError
from datetime import datetime
from backend.core.contracts import TestSpecification, RunResult, Classification, Scores

def test_test_case_valid():
    """
    Tests that a `TestSpecification` object can be created with valid data.
    """
    data = {
        "case_id": "injection-001",
        "suite_id": "injection",
        "prompt": "Test prompt"
    }
    case = TestSpecification(**data)
    assert case.case_id == "injection-001"
    assert case.suite_id == "injection"
    assert case.prompt == "Test prompt"

def test_test_case_invalid():
    """
    Tests that creating a `TestSpecification` object with missing required
    fields raises a Pydantic `ValidationError`.
    """
    with pytest.raises(ValidationError):
        TestSpecification(suite_id="injection", prompt="Test prompt")

def test_run_result_valid():
    """
    Tests that a `RunResult` object can be created with valid data,
    including nested classification and scores.
    """
    data = {
        "case_id": "injection-001",
        "suite_id": "injection",
        "run_id": "run-123",
        "model_id": "gpt-4-turbo",
        "timestamp_utc": datetime.now(),
        "classification": {"primary": "pass"},
        "scores": {"accuracy": 1.0}
    }
    result = RunResult(**data)
    assert result.run_id == "run-123"
    assert result.classification.primary == "pass"
    assert result.scores.accuracy == 1.0

def test_run_result_invalid():
    """
    Tests that creating a `RunResult` object with a missing `run_id`
    raises a Pydantic `ValidationError`.
    """
    with pytest.raises(ValidationError):
        RunResult(
            case_id="injection-001",
            suite_id="injection",
            model_id="gpt-4-turbo",
            timestamp_utc=datetime.now()
        )