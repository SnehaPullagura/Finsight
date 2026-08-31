import React from 'react';

interface HealthScoreGaugeProps {
  score: number;
  grade: string;
}

export const HealthScoreGauge: React.FC<HealthScoreGaugeProps> = ({ score, grade }) => {
  const circumference = 2 * Math.PI * 42;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const getColor = () => {
    if (score >= 80) return '#10B981'; // Emerald
    if (score >= 65) return '#6366F1'; // Indigo
    if (score >= 50) return '#F59E0B'; // Amber
    return '#EF4444'; // Rose
  };

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r="42"
            stroke="currentColor"
            strokeWidth="10"
            className="text-slate-800"
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r="42"
            stroke={getColor()}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-extrabold text-white mono leading-none">{score}</span>
          <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-widest mt-1">/ 100</span>
        </div>
      </div>
      <div className="mt-3 px-3 py-1 rounded-full bg-slate-800 text-xs font-extrabold text-white border border-slate-700">
        {grade}
      </div>
    </div>
  );
};
