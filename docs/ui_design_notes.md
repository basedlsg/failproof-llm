# UI Design Notes: Read-Only Dashboard

This document specifies the UI contract for the read-only dashboard.

## 1. Route Map

The dashboard will have the following routes:

| Path | Page Component | Description |
|---|---|---|
| `/runs` | `RunsPage` | Displays a list of all test runs. |
| `/runs/:id` | `RunDetailPage` | Shows the summary and results of a specific run. |
| `/cases/:id` | `CaseDetailPage` | Provides detailed information about a single test case. |
| `/compare` | `ComparePage` | Allows side-by-side comparison of two runs (`?runA=<run_id>&runB=<run_id>`). |

## 2. Component Prop Shapes

This section defines the props for each major UI component.

### `RunList`

Displays a table of test runs.

```typescript
interface Run {
  id: string;
  name: string;
  timestamp: string;
  pass_rate: number;
  total_cases: number;
}

interface RunListProps {
  runs: Run[];
}
```

### `RunSummary`

Shows high-level details and metrics for a single run.

```typescript
interface RunSummaryProps {
  run: {
    id: string;
    name: string;
    timestamp: string;
    pass_count: number;
    fail_count: number;
    total_cases: number;
    pass_rate: number;
    cases: TestCase[];
  };
}

interface TestCase {
  id: string;
  status: 'pass' | 'fail';
  model_output: string;
  expected_output: string;
}
```

### `CaseDetail`

Displays the full details of a single test case.

```typescript
interface CaseDetailProps {
  testCase: {
    id: string;
    prompt: string;
    model_output: string;
    expected_output: string;
    classifier: string;
    score: number;
  };
}
```

### `FailureFilters`

Provides options to filter failed test cases.

```typescript
interface FailureFiltersProps {
  onFilterChange: (filters: { classifier?: string; score_threshold?: number }) => void;
}
```

### `CompareRuns`

Compares two runs side-by-side.

```typescript
interface CompareRunsProps {
  runA: RunSummaryProps['run'];
  runB: RunSummaryProps['run'];
}
```

### `ExportButton`

Allows users to download data.

```typescript
interface ExportButtonProps {
  data: any[];
  filename: string;
}
```

## 3. "Compare Runs" Data Contract (`/compare?runA&runB`)

The `/compare` route will fetch data for two runs and structure it as follows:

```json
{
  "runA": {
    "id": "run_id_A",
    "name": "Run A Name",
    "timestamp": "2025-08-10T10:00:00Z",
    "pass_count": 85,
    "fail_count": 15,
    "total_cases": 100,
    "pass_rate": 0.85,
    "cases": [
      { "id": "case_1", "status": "pass", "..." },
      { "id": "case_2", "status": "fail", "..." }
    ]
  },
  "runB": {
    "id": "run_id_B",
    "name": "Run B Name",
    "timestamp": "2025-08-09T12:00:00Z",
    "pass_count": 90,
    "fail_count": 10,
    "total_cases": 100,
    "pass_rate": 0.90,
    "cases": [
      { "id": "case_1", "status": "pass", "..." },
      { "id": "case_2", "status": "pass", "..." }
    ]
  }
}
```

## 4. ASCII Wireframes

### Runs Page (`/runs`)

```
+--------------------------------------------------------------------+
| All Test Runs                                [Export All]          |
+--------------------------------------------------------------------+
|                                                                    |
| [RunList]                                                          |
| +----------------------------------------------------------------+ |
| | Name       | Timestamp           | Pass Rate | Total Cases    | |
| |------------|---------------------|-----------|----------------| |
| | Run 1      | 2025-08-10 10:00:00 | 85%       | 100            | |
| | Run 2      | 2025-08-09 12:00:00 | 90%       | 100            | |
| +----------------------------------------------------------------+ |
|                                                                    |
+--------------------------------------------------------------------+
```

### Run Detail Page (`/runs/:id`)

```
+--------------------------------------------------------------------+
| Run: [Run Name]                                    [Export Run]    |
+--------------------------------------------------------------------+
|                                                                    |
| [RunSummary]                                                       |
| +----------------------+ +---------------------------------------+ |
| | Pass/Fail Chart      | | Pass: 85                              | |
| | [|||||     ]         | | Fail: 15                              | |
| |                      | | Total: 100                            | |
| +----------------------+ +---------------------------------------+ |
|                                                                    |
| [FailureFilters]                                                   |
| Filter by Classifier: [Dropdown]  Score Threshold: [Input]         |
|                                                                    |
| [TestCaseList]                                                     |
| +----------------------------------------------------------------+ |
| | Case ID    | Status | Details                                | |
| |------------|--------|----------------------------------------| |
| | case_2     | fail   | [View]                                 | |
| +----------------------------------------------------------------+ |
+--------------------------------------------------------------------+
```

### Compare Runs Page (`/compare`)

```
+------------------------------------------------------------------------------------+
| Compare Runs                                                                       |
+------------------------------------------------------------------------------------+
|                                                                                    |
|                      [Run A Dropdown]      vs.      [Run B Dropdown]                 |
|                                                                                    |
| [CompareRuns]                                                                      |
| +------------------------------------------+---------------------------------------+ |
| | Run A: [Name]                            | Run B: [Name]                         | |
| | Pass Rate: 85%                           | Pass Rate: 90%                        | |
| |                                          |                                       | |
| | Side-by-side comparison of metrics...    |                                       | |
| |                                          |                                       | |
| | Regressions:                             |                                       | |
| | - case_2 (pass -> fail)                  |                                       | |
| +------------------------------------------+---------------------------------------+ |
|                                                                                    |
+------------------------------------------------------------------------------------+