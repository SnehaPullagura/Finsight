import React, { useState } from "react";
import { UploadCloud, CheckCircle2, ArrowRight, Table, AlertCircle } from "lucide-react";

export const EnterpriseDataImportMapper: React.FC = () => {
  const [mappings, setMappings] = useState([
    { sourceHeader: "Company_Name", targetField: "company_name", sample: "Stark Industries", status: "mapped" },
    { sourceHeader: "Contact_Email", targetField: "email", sample: "tony@stark.internal", status: "mapped" },
    { sourceHeader: "Phone_Number", targetField: "phone", sample: "+1-555-0199", status: "mapped" },
    { sourceHeader: "Annual_Rev", targetField: "annual_revenue", sample: "$15,000,000", status: "mapped" }
  ]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <UploadCloud className="w-5 h-5 text-emerald-400" />
            CRM Schema Mapping & Data Ingestion Studio
          </h3>
          <p className="text-xs text-slate-400">Map third-party CSV/Excel fields to ClientFlow CRM dimensional entities</p>
        </div>
        <button className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-1.5 rounded-lg text-xs font-semibold shadow-lg transition-colors">
          Execute Import Batch
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Source Column</th>
              <th className="p-3 text-center">Mapping</th>
              <th className="p-3">ClientFlow CRM Field</th>
              <th className="p-3">Sample Preview</th>
              <th className="p-3 text-right">Validation</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {mappings.map((m, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-mono text-slate-300">{m.sourceHeader}</td>
                <td className="p-3 text-center text-slate-500"><ArrowRight className="w-4 h-4 inline" /></td>
                <td className="p-3 font-semibold text-emerald-400">{m.targetField}</td>
                <td className="p-3 text-slate-400">{m.sample}</td>
                <td className="p-3 text-right">
                  <span className="text-emerald-400 font-medium flex items-center justify-end gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Ready
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
