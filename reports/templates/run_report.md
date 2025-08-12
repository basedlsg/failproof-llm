# LLM Test Run Report

**Run ID:** `{{ run_id }}`
**Timestamp:** `{{ timestamp }}`

---

## 1. Overall Score & KPIs

| Metric                 | Value | Trend |
| ---------------------- | ----- | ----- |
| **Overall Score**      | `{{ overall_score }}` | `{{ score_trend }}` |
| Pass Rate              | `{{ pass_rate }}`     | `{{ pass_rate_trend }}` |
| Average Response Time  | `{{ avg_response_time }}` | `{{ response_time_trend }}` |

---

## 2. Results by Test Suite

| Suite Name           | Cases Run | Pass | Fail | Average Score |
| -------------------- | --------- | ---- | ---- | ------------- |
| `{{ suite_name }}`   | `{{ suite_cases_run }}` | `{{ suite_pass_count }}` | `{{ suite_fail_count }}` | `{{ suite_avg_score }}` |
| ...                  | ...       | ...  | ...  | ...           |

---

## 3. Failed Test Cases

| Case ID                               | Suite                | Failure Reason      |
| ------------------------------------- | -------------------- | ------------------- |
| [`{{ failed_case_id }}`](/cases/`{{ failed_case_id }}`) | `{{ failed_case_suite }}` | `{{ failed_case_reason }}` |
| ...                                   | ...                  | ...                 |

---

## 4. Reproducibility

To reproduce this test run, use the following configuration and commands:

**Configuration:**
```json
{
  "model_id": "{{ model_id }}",
  "test_suites": [
    "{{ suite_1 }}",
    "{{ suite_2 }}"
  ],
  "run_parameters": {
    "temperature": "{{ temperature }}",
    "max_tokens": "{{ max_tokens }}"
  }
}
```

**Command:**
```bash
failproof-llm run --config ./path/to/config.json