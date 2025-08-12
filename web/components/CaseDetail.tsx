import React from 'react';
import useSWR from 'swr';
import { components } from '../lib/api-client';
import { useRouter } from 'next/router';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

const CaseDetail: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const { data, error } = useSWR<components['schemas']['RunResult']>(id ? `/api/proxy/api/v1/cases/${id}` : null, fetcher);

  if (error) return <div>Failed to load case</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>Case Detail: {data.case_id}</h1>
      <p>Run ID: {data.run_id}</p>
      <p>Suite ID: {data.suite_id}</p>
      <p>Model ID: {data.model_id}</p>
      <p>Timestamp: {data.timestamp_utc}</p>
      <h2>Prompt</h2>
      <pre>{data.prompt}</pre>
      <h2>Response</h2>
      <pre>{data.response}</pre>
      <h2>Classification</h2>
      <pre>{JSON.stringify(data.classification, null, 2)}</pre>
      <h2>Score</h2>
      <p>{data.score}</p>
      {data.error && (
        <>
          <h2>Error</h2>
          <pre>{data.error}</pre>
        </>
      )}
    </div>
  );
};

export default CaseDetail;