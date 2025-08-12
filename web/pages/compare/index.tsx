import React, { useState } from 'react';
import useSWR from 'swr';
import CompareRuns from '../../components/CompareRuns';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

const ComparePage = () => {
  const [runAId, setRunAId] = useState<string | null>(null);
  const [runBId, setRunBId] = useState<string | null>(null);

  const { data: runsData } = useSWR('/api/runs', fetcher);
  const { data: runAData } = useSWR(runAId ? `/api/runs/${runAId}` : null, fetcher);
  const { data: runBData } = useSWR(runBId ? `/api/runs/${runBId}` : null, fetcher);

  return (
    <div>
      <h1>Compare Runs</h1>
      <select onChange={(e) => setRunAId(e.target.value)}>
        <option value="">Select Run A</option>
        {runsData?.map((run: any) => (
          <option key={run.id} value={run.id}>
            {run.name}
          </option>
        ))}
      </select>
      <select onChange={(e) => setRunBId(e.target.value)}>
        <option value="">Select Run B</option>
        {runsData?.map((run: any) => (
          <option key={run.id} value={run.id}>
            {run.name}
          </option>
        ))}
      </select>
      {runAData && runBData && <CompareRuns runA={runAData} runB={runBData} />}
    </div>
  );
};

export default ComparePage;