import React from 'react';

interface ExportButtonProps {
  data: any[];
  filename: string;
}

const ExportButton: React.FC<ExportButtonProps> = ({ data, filename }) => {
  const handleExport = () => {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <button onClick={handleExport}>
      Export
    </button>
  );
};

export default ExportButton;