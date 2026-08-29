import React, { useEffect, useState } from "react";
import { Plus, CheckSquare, Clock, AlertCircle } from "lucide-react";
import { api } from "../../services/api";
import { Task } from "../../types";

export const TasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => { loadTasks(); }, []);
  const loadTasks = () => { api.getTasks().then(res => setTasks(res.data)).catch(console.error); };

  const handleComplete = async (id: string) => {
    await api.completeTask(id);
    loadTasks();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Task Management</h1>
        <p className="text-xs text-slate-500">Scheduled action items, recurring routines, and reminders</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs divide-y divide-slate-100">
        {tasks.map(t => (
          <div key={t.id} className="p-4 flex items-center justify-between hover:bg-slate-50">
            <div className="flex items-center gap-3">
              <input type="checkbox" checked={t.status === "completed"} onChange={() => handleComplete(t.id)} className="rounded text-emerald-600 focus:ring-0" />
              <div>
                <div className={`text-xs font-bold ${t.status === "completed" ? "line-through text-slate-400" : "text-slate-900"}`}>{t.title}</div>
                <div className="text-[11px] text-slate-500">{t.description || "No description"}</div>
              </div>
            </div>
            <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${t.priority === 'urgent' ? 'bg-rose-100 text-rose-800' : 'bg-slate-100 text-slate-700'}`}>
              {t.priority}
            </span>
          </div>
        ))}
        {tasks.length === 0 && <div className="p-8 text-center text-xs text-slate-400">All tasks completed!</div>}
      </div>
    </div>
  );
};
