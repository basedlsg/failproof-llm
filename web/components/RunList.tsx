import React from 'react';
import useSWR from 'swr';
import { components } from '../lib/api-client';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

const RunList: React.FC = () => {
  const { data, error } = useSWR<components['schemas']['Run'][]>('/api/proxy/api/v1/runs', fetcher);

  if (error) return <div>Failed to load runs</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>Test Runs</h1>
      <ul>
        {data.map((run) => (
          <li key={run.run_id}>
            <a href={`/runs/${run.run_id}`}>
              {run.run_id} - {run.model_id}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RunList;