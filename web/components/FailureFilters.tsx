import React from 'react';

interface FailureFiltersProps {
  onFilterChange: (filters: { classifier?: string; score_threshold?: number }) => void;
}

const FailureFilters: React.FC<FailureFiltersProps> = ({ onFilterChange }) => {
  return (
    <div>
      <label>
        Filter by Classifier:
        <input type="text" onChange={(e) => onFilterChange({ classifier: e.target.value })} />
      </label>
      <label>
        Score Threshold:
        <input type="number" onChange={(e) => onFilterChange({ score_threshold: parseFloat(e.target.value) })} />
      </label>
    </div>
  );
};

export default FailureFilters;