import React, { useState } from "react";
import { LayoutGrid, Plus, Trash2, Eye, Save } from "lucide-react";

export const EnterpriseFormBuilderStudio: React.FC = () => {
  const [fields, setFields] = useState([
    { id: "1", label: "Estimated Annual Budget", type: "Currency", required: true },
    { id: "2", label: "Executive Decision Maker", type: "Lookup (Contact)", required: true },
    { id: "3", label: "Contract Target Go-Live Date", type: "Date", required: false },
    { id: "4", label: "Competitive Landscape", type: "Multi-Select Picklist", required: false }
  ]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <LayoutGrid className="w-5 h-5 text-emerald-400" />
            Dynamic CRM Layout & Schema Builder
          </h3>
          <p className="text-xs text-slate-400">Design custom object layouts, validation rules, and dependent fields</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-lg transition-colors">
          <Save className="w-4 h-4" />
          Save Form Layout
        </button>
      </div>

      <div className="space-y-3">
        {fields.map(f => (
          <div key={f.id} className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{f.label}</div>
              <div className="text-[10px] text-slate-500">{f.type} {f.required && "• Required"}</div>
            </div>
            <span className="text-xs text-emerald-400 font-medium">Active</span>
          </div>
        ))}
      </div>
    </div>
  );
};
