import React, { useState } from "react";
import { Database, ShieldCheck, CheckCircle2, History } from "lucide-react";

export const EnterpriseDeltaLakeConverterStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-emerald-400" />
            Delta Lake ACID & Time-Travel Lakehouse Converter
          </h3>
          <p className="text-xs text-slate-400">Upgrades Parquet datasets with Delta Lake ACID transaction logs and 30-day time travel</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Delta ACID Enabled
        </span>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Delta Table: s3://clientflow-lakehouse-analytics-prod/delta/deals</span>
          <span className="text-xs text-emerald-400 font-semibold">ACID v4 Active</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Full ACID transaction support with snapshot isolation</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>30-Day time travel and point-in-time rollback enabled</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Zero-copy cloning for rapid analytics development sandbox</span>
          </div>
        </div>
      </div>
    </div>
  );
};
