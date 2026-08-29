import React from "react";
import { Settings, Shield, Users, Sliders } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export const SettingsPage: React.FC = () => {
  const { organization, user } = useAuth();

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Organization Settings</h1>
        <p className="text-xs text-slate-500">Workspace preferences, RBAC access control, and security</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
        <h3 className="text-xs font-bold text-slate-900">Tenant Profile</h3>
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div>
            <label className="text-slate-400 block mb-1">Organization Name</label>
            <input disabled className="w-full bg-slate-50 border p-2 rounded text-slate-700" value={organization?.name || "Apex Global"} />
          </div>
          <div>
            <label className="text-slate-400 block mb-1">Plan Tier</label>
            <input disabled className="w-full bg-slate-50 border p-2 rounded text-slate-700 uppercase font-semibold text-emerald-600" value={organization?.plan_tier || "Enterprise"} />
          </div>
        </div>
      </div>
    </div>
  );
};
