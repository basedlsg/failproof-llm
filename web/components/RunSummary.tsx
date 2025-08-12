import React from 'react';
import useSWR from 'swr';
import { components } from '../lib/api-client';
import { useRouter } from 'next/router';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

const RunSummary: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const { data, error } = useSWR<components['schemas']['Run']>(id ? `/api/proxy/api/v1/runs/${id}` : null, fetcher);

  if (error) return <div>Failed to load run</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>Run Summary: {data.run_id}</h1>
      <p>Model: {data.model_id}</p>
      <p>Timestamp: {data.timestamp_utc}</p>
      <h2>Suite Stats: {data.suite_stats.suite_id}</h2>
      <ul>
        <li>Total Cases: {data.suite_stats.total_cases}</li>
        <li>Pass Count: {data.suite_stats.pass_count}</li>
        <li>Fail Count: {data.suite_stats.fail_count}</li>
        <li>Error Count: {data.suite_stats.error_count}</li>
      </ul>
      <a href={`/api/runs/${id}/report.md`}>View Full Report</a>
    </div>
  );
};

export default RunSummary;