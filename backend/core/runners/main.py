import json
from datetime import datetime, timezone
from uuid import uuid4

from backend.adapters.model_client import ModelClient
from backend.core.contracts import CaseResult, RunResult, TestSpecification as TestCase


class Runner:
    def __init__(self, model_client: ModelClient):
        self.model_client = model_client

    def run_suite(self, suite_path: str) -> RunResult:
        test_cases = []
        with open(suite_path, "r") as f:
            for line in f:
                data = json.loads(line)
                test_cases.append(TestCase(**data))

        case_results = []
        for case in test_cases:
            output = self.model_client.execute(prompt=case.prompt)
            case_results.append(
                CaseResult(
                    test_case=case,
                    output=output,
                    tokens_used=0,  # Placeholder
                    latency_ms=0,  # Placeholder
                )
            )

        return RunResult(
            id=str(uuid4()),
            suite_path=suite_path,
            created_at=datetime.now(timezone.utc),
            results=case_results,
        )