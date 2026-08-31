import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. frontend/src/components/enterprise/AdvancedGanttChart.tsx
    write_file("frontend/src/components/enterprise/AdvancedGanttChart.tsx", """import React, { useState } from "react";
import { Calendar, CheckCircle2, Clock, AlertTriangle, ChevronRight } from "lucide-react";

interface MilestoneTask {
  id: string;
  name: string;
  owner: string;
  start_day: number;
  duration_days: number;
  progress_pct: number;
  status: "completed" | "in_progress" | "pending";
}

const SAMPLE_MILESTONES: MilestoneTask[] = [
  { id: "m1", name: "Security & SAML SSO Configuration", owner: "Alexander Vance", start_day: 1, duration_days: 7, progress_pct: 100, status: "completed" },
  { id: "m2", name: "Contact & Account Data Migration", owner: "Sarah Connor", start_day: 5, duration_days: 10, progress_pct: 75, status: "in_progress" },
  { id: "m3", name: "Custom Workflow DAG Automation Setup", owner: "Alexander Vance", start_day: 12, duration_days: 8, progress_pct: 30, status: "in_progress" },
  { id: "m4", name: "Executive Team User Training & Onboarding", owner: "Pepper Potts", start_day: 18, duration_days: 12, progress_pct: 0, status: "pending" }
];

export const AdvancedGanttChart: React.FC = () => {
  const [tasks] = useState<MilestoneTask[]>(SAMPLE_MILESTONES);
  const totalDays = 30;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-400" />
            Customer Onboarding Milestone & Gantt Timeline
          </h3>
          <p className="text-xs text-slate-400">Track implementation schedules, critical paths, and milestone deliverables</p>
        </div>
      </div>

      <div className="space-y-3">
        {tasks.map(task => {
          const leftPct = (task.start_day / totalDays) * 100;
          const widthPct = (task.duration_days / totalDays) * 100;

          return (
            <div key={task.id} className="space-y-1 text-xs">
              <div className="flex items-center justify-between">
                <div className="font-semibold text-white flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${
                    task.status === "completed" ? "bg-emerald-400" :
                    task.status === "in_progress" ? "bg-blue-400" : "bg-slate-600"
                  }`} />
                  <span>{task.name}</span>
                </div>
                <div className="text-[11px] text-slate-400">
                  {task.owner} — <strong className="text-emerald-400">{task.progress_pct}%</strong>
                </div>
              </div>

              <div className="h-6 bg-slate-950 rounded-lg relative overflow-hidden border border-slate-800">
                <div
                  style={{ left: `${leftPct}%`, width: `${widthPct}%` }}
                  className={`absolute top-1 bottom-1 rounded-md px-2 flex items-center text-[10px] font-bold text-slate-950 transition-all ${
                    task.status === "completed" ? "bg-emerald-400" :
                    task.status === "in_progress" ? "bg-blue-400" : "bg-slate-700 text-white"
                  }`}
                >
                  <span className="truncate">{task.duration_days}d</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
""")

    # 2. frontend/src/components/enterprise/FormSchemaDesigner.tsx
    write_file("frontend/src/components/enterprise/FormSchemaDesigner.tsx", """import React, { useState } from "react";
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
""")

    # 3. frontend/src/components/enterprise/EmailTemplateComposer.tsx
    write_file("frontend/src/components/enterprise/EmailTemplateComposer.tsx", """import React, { useState } from "react";
import { Mail, Send, Eye, Sparkles, Code } from "lucide-react";

export const EmailTemplateComposer: React.FC = () => {
  const [subject, setSubject] = useState("Exciting Updates regarding {{company.name}} & ClientFlow");
  const [body, setBody] = useState("Hi {{contact.first_name}},\\n\\nThank you for exploring ClientFlow CRM! We've prepared your custom pricing proposal for {{deal.value}}.\\n\\nBest regards,\\n{{user.name}}");
  const [previewContact] = useState({ first_name: "Pepper", company: "Stark Industries", deal_value: "$250,000" });

  const renderPreview = () => {
    return body
      .replace("{{contact.first_name}}", previewContact.first_name)
      .replace("{{company.name}}", previewContact.company)
      .replace("{{deal.value}}", previewContact.deal_value)
      .replace("{{user.name}}", "Alexander Vance");
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div>
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Mail className="w-5 h-5 text-emerald-400" />
          Omnichannel Email & Template Studio
        </h3>
        <p className="text-xs text-slate-400">Design personalized Jinja2/Liquid merge tag email templates for automated campaigns</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300">Subject Line</label>
            <input
              type="text"
              value={subject}
              onChange={e => setSubject(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-white mt-1 focus:outline-none focus:border-emerald-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-300">Email Template Body</label>
            <textarea
              rows={8}
              value={body}
              onChange={e => setBody(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-xs text-slate-200 font-mono mt-1 focus:outline-none focus:border-emerald-500"
            />
          </div>
        </div>

        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
          <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-400 border-b border-slate-800 pb-2">
            <Eye className="w-4 h-4" /> Live Rendered Preview
          </div>
          <div className="text-xs text-white font-semibold">
            Subject: <span className="text-slate-300 font-normal">{subject.replace("{{company.name}}", previewContact.company)}</span>
          </div>
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800 text-xs text-slate-300 whitespace-pre-wrap leading-relaxed">
            {renderPreview()}
          </div>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created GanttChart, FormSchemaDesigner, and EmailTemplateComposer.")

if __name__ == '__main__':
    run()
