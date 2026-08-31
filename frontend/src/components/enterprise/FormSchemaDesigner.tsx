import React, { useState } from "react";
import { Layers, Plus, Trash2, Code, Eye, CheckCircle2 } from "lucide-react";

interface FieldDef {
  id: string;
  name: string;
  type: "text" | "number" | "select" | "date" | "boolean";
  required: boolean;
  options?: string[];
}

export const FormSchemaDesigner: React.FC = () => {
  const [fields, setFields] = useState<FieldDef[]>([
    { id: "1", name: "Annual Budget ($)", type: "number", required: true },
    { id: "2", name: "Deployment Target", type: "select", required: true, options: ["AWS", "GCP", "Azure", "On-Premises"] },
    { id: "3", name: "Target Go-Live Date", type: "date", required: false }
  ]);

  const addField = () => {
    setFields([
      ...fields,
      { id: Date.now().toString(), name: "New Field", type: "text", required: false }
    ]);
  };

  const removeField = (id: string) => {
    setFields(fields.filter(f => f.id !== id));
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-emerald-400" />
            Dynamic Form & Entity Schema Builder
          </h3>
          <p className="text-xs text-slate-400">Design dynamic fields and validation rules for CRM entities</p>
        </div>
        <button
          onClick={addField}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-lg"
        >
          <Plus className="w-3.5 h-3.5" /> Add Field
        </button>
      </div>

      <div className="space-y-3">
        {fields.map(f => (
          <div key={f.id} className="grid grid-cols-12 gap-3 items-center bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs">
            <div className="col-span-6">
              <input
                type="text"
                value={f.name}
                onChange={e => setFields(fields.map(item => item.id === f.id ? { ...item, name: e.target.value } : item))}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white"
              />
            </div>
            <div className="col-span-3">
              <select
                value={f.type}
                onChange={e => setFields(fields.map(item => item.id === f.id ? { ...item, type: e.target.value as any } : item))}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white"
              >
                <option value="text">Text</option>
                <option value="number">Number</option>
                <option value="select">Dropdown</option>
                <option value="date">Date</option>
                <option value="boolean">Checkbox</option>
              </select>
            </div>
            <div className="col-span-2 flex items-center gap-1.5 text-slate-400">
              <input
                type="checkbox"
                checked={f.required}
                onChange={e => setFields(fields.map(item => item.id === f.id ? { ...item, required: e.target.checked } : item))}
                className="rounded border-slate-700"
              />
              <span>Required</span>
            </div>
            <div className="col-span-1 flex justify-end">
              <button onClick={() => removeField(f.id)} className="text-slate-500 hover:text-rose-400">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
