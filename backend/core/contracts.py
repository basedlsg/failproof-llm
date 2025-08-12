from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class TestSpecification(BaseModel):
    case_id: str = Field(..., description="A unique identifier for the test case, e.g., 'injection-001'.")
    suite_id: str = Field(..., description="The ID of the test suite this case belongs to, e.g., 'injection'.")
    prompt: str = Field(..., description="The exact text to be sent to the LLM.")
    prompt_vars: Optional[Dict[str, str]] = Field(None, description="A dictionary of variables to be interpolated into the prompt string.")
    expected_response: Optional[str] = Field(None, description="A description or pattern of the expected response. Can be a regex or a simple string.")
    expected_classification: Optional[str] = Field(None, description="The primary classification expected for this test case if it behaves correctly.", pattern="^(pass|fail)$")
    tags: Optional[List[str]] = Field(default_factory=list, description="A list of tags for categorization and filtering.")

class Classification(BaseModel):
    primary: str = Field(..., description="The main classification, e.g., 'pass', 'fail', 'refusal'.")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional details or secondary classifications.")

class Scores(BaseModel):
    accuracy: float = Field(..., description="Binary score: 1 for a pass, 0 for a fail.", ge=0, le=1)

class CaseResult(BaseModel):
    test_case: 'TestSpecification' = Field(..., description="The test case that was run.")
    output: str = Field(..., description="The output from the model.")
    tokens_used: int = Field(..., description="Number of tokens used.")
    latency_ms: int = Field(..., description="Latency in milliseconds.")

class RunResult(BaseModel):
    # Core identifier 
    run_id: str = Field(..., description="A unique identifier for the entire test run.")
    
    # Fields used by runner
    suite_path: Optional[str] = Field(None, description="Path to the test suite file.")
    created_at: Optional[datetime] = Field(None, description="The timestamp of when the test run was created.")
    results: Optional[List['CaseResult']] = Field(None, description="List of individual case results.")
    
    # Fields used by storage/contracts  
    case_id: Optional[str] = Field(None, description="The ID of the TestCase that was run.")
    suite_id: Optional[str] = Field(None, description="The ID of the test suite.")
    model_id: Optional[str] = Field(None, description="The identifier of the model that was tested, e.g., 'gpt-4-turbo'.")
    timestamp_utc: Optional[datetime] = Field(None, description="The ISO 8601 timestamp of when the test was executed.")
    raw_response: Optional[str] = Field(None, description="The complete, unmodified response from the LLM.")
    error: Optional[str] = Field(None, description="Any error message captured during the run. Null if successful.")
    classification: Optional[Classification] = Field(None, description="The deterministic classification assigned by the Classifier.")
    scores: Optional[Scores] = Field(None, description="Quantitative scores assigned by the Scorer.")
    
    @model_validator(mode='before')
    def handle_id_field(cls, values):
        # Allow 'id' to be used as an alias for 'run_id'
        if isinstance(values, dict):
            if 'id' in values and 'run_id' not in values:
                values['run_id'] = values.pop('id')
        return values