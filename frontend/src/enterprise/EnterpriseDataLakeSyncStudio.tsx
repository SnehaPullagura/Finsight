import React, { useState } from "react";
import { Database, RefreshCw, CheckCircle2, Server } from "lucide-react";

export const EnterpriseDataLakeSyncStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-emerald-400" />
            Enterprise Data Lakehouse Parquet Sync Engine
          </h3>
          <p className="text-xs text-slate-400">Zero-ETL automated replication of CRM entities to Snowflake, BigQuery & Databricks</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <RefreshCw className="w-4 h-4" />
          Trigger Lakehouse Sync
        </button>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Active Lakehouse Destination: s3://clientflow-lakehouse-analytics-prod</span>
          <span className="text-xs text-emerald-400 font-semibold">Synced 2m ago</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Partitioned Apache Parquet format with Snappy compression</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Automated schema evolution and drift detection active</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Field-level blind indexing for encrypted PII replication</span>
          </div>
        </div>
      </div>
    </div>
  );
};
