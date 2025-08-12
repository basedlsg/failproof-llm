import json
import os
import unittest
from unittest.mock import MagicMock

from backend.core.contracts import TestSpecification as TestCase
from backend.core.runners.main import Runner


class TestRunner(unittest.TestCase):
    def setUp(self):
        self.mock_model_client = MagicMock()
        self.runner = Runner(model_client=self.mock_model_client)
        self.test_suite_path = "test_suite.jsonl"

    def tearDown(self):
        if os.path.exists(self.test_suite_path):
            os.remove(self.test_suite_path)

    def test_run_suite(self):
        # Arrange
        test_cases = [
            TestCase(
                case_id="1",
                suite_id="test_suite",
                prompt="Prompt 1",
                tags=["test"],
                expected_response="Truth 1",
            ),
            TestCase(
                case_id="2",
                suite_id="test_suite",
                prompt="Prompt 2",
                tags=["test"],
                expected_response="Truth 2",
            ),
        ]
        with open(self.test_suite_path, "w") as f:
            for case in test_cases:
                f.write(json.dumps(case.model_dump()) + "\n")

        self.mock_model_client.execute.side_effect = [
            "Output 1",
            "Output 2",
        ]

        # Act
        run_result = self.runner.run_suite(self.test_suite_path)

        # Assert
        self.assertEqual(len(run_result.results), 2)
        self.assertEqual(run_result.results[0].output, "Output 1")
        self.assertEqual(run_result.results[1].output, "Output 2")
        self.assertEqual(run_result.suite_path, self.test_suite_path)
        self.assertEqual(
            self.mock_model_client.execute.call_count, 2
        )
        self.mock_model_client.execute.assert_any_call(
            prompt="Prompt 1"
        )
        self.mock_model_client.execute.assert_any_call(
            prompt="Prompt 2"
        )


if __name__ == "__main__":
    unittest.main()