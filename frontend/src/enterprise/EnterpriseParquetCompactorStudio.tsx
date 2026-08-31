import React, { useState } from "react";
import { Layers, Database, CheckCircle2, RefreshCw } from "lucide-react";

export const EnterpriseParquetCompactorStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-emerald-400" />
            Parquet Small-File Compaction & Lakehouse Optimizer
          </h3>
          <p className="text-xs text-slate-400">Automated file layout optimization reducing query latency on S3/GCS data lakes</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Optimized
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Small Files Merged</span>
          <div className="text-2xl font-bold text-white">1,420 Files</div>
          <span className="text-[10px] text-slate-400">Compacted to 213 Optimal Blocks</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Query Latency Reduction</span>
          <div className="text-2xl font-bold text-emerald-400">-64.5% Faster</div>
          <span className="text-[10px] text-emerald-400">Athena & BigLake Acceleration</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Storage Overhead Saved</span>
          <div className="text-2xl font-bold text-emerald-400">5.96 GB</div>
          <span className="text-[10px] text-slate-400">Snappy Compression Verified</span>
        </div>
      </div>
    </div>
  );
};
