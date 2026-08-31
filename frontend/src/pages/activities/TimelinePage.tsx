import React, { useEffect, useState } from "react";
import { Clock, Phone, Mail, CheckCircle2, MessageSquare, Plus } from "lucide-react";
import { api } from "../../services/api";
import { Activity } from "../../types";

export const TimelinePage: React.FC = () => {
  const [activities, setActivities] = useState<Activity[]>([
    { id: "1", tenant_id: "org-1", entity_type: "deal", entity_id: "d1", activity_type: "CALL", title: "Discovery Call with CTO", description: "Discussed integration architecture and security compliances.", performed_at: new Date().toISOString(), metadata_json: {}, created_at: new Date().toISOString() },
    { id: "2", tenant_id: "org-1", entity_type: "lead", entity_id: "l1", activity_type: "EMAIL", title: "Sent Proposal Summary Deck", description: "Delivered pricing tiers and enterprise SLA documentation.", performed_at: new Date(Date.now() - 3600000).toISOString(), metadata_json: {}, created_at: new Date().toISOString() },
    { id: "3", tenant_id: "org-1", entity_type: "company", entity_id: "c1", activity_type: "NOTE", title: "Quarterly Executive Alignment", description: "Customer success target set to 100% onboarding milestone completion.", performed_at: new Date(Date.now() - 86400000).toISOString(), metadata_json: {}, created_at: new Date().toISOString() }
  ]);

  const getIcon = (type: string) => {
    switch (type) {
      case "CALL": return <Phone className="w-4 h-4 text-blue-600" />;
      case "EMAIL": return <Mail className="w-4 h-4 text-purple-600" />;
      default: return <MessageSquare className="w-4 h-4 text-emerald-600" />;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Unified Activity Timeline</h1>
        <p className="text-xs text-slate-500">Cross-entity stream for calls, emails, meetings, and updates</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-6">
        <div className="relative pl-6 border-l-2 border-slate-200 space-y-6">
          {activities.map((a) => (
            <div key={a.id} className="relative group">
              <div className="absolute -left-[31px] top-0.5 p-1.5 rounded-full bg-white border-2 border-slate-200 group-hover:border-emerald-500 transition-colors">
                {getIcon(a.activity_type)}
              </div>
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 space-y-1">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-slate-900">{a.title}</span>
                  <span className="text-[11px] text-slate-400">{new Date(a.performed_at).toLocaleString()}</span>
                </div>
                <p className="text-xs text-slate-600">{a.description}</p>
                <div className="text-[10px] font-semibold text-slate-400 uppercase pt-1">
                  Target: {a.entity_type} #{a.entity_id}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
