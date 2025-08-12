import React from 'react';
import { RunSummaryProps } from './RunSummary';

interface CompareRunsProps {
  runA: RunSummaryProps['run'];
  runB: RunSummaryProps['run'];
}

const CompareRuns: React.FC<CompareRunsProps> = ({ runA, runB }) => {
  return (
    <div>
      <div>
        <h3>{runA.name}</h3>
        <p>Pass Rate: {runA.pass_rate}%</p>
      </div>
      <div>
        <h3>{runB.name}</h3>
        <p>Pass Rate: {runB.pass_rate}%</p>
      </div>
    </div>
  );
};

export default CompareRuns;