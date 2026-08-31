import React, { useState } from "react";
import { ShieldCheck, Download, FileText, CheckCircle2 } from "lucide-react";
import { api } from "../../services/api";

export const GovernancePage: React.FC = () => {
  const [email, setEmail] = useState("admin@clientflow.internal");
  const [exportData, setExportData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleExport = async () => {
    setIsLoading(true);
    try {
      const res = await api.post("/governance/dsr/export", { subject_email: email });
      setExportData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            GDPR / CCPA Data Subject Rights (DSR) Portal
          </h3>
          <p className="text-xs text-slate-400">Article 15 Subject Access Request generator and right-to-be-forgotten anonymizer</p>
        </div>

        <div className="flex items-center gap-3">
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            className="w-80 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
            placeholder="Subject Email Address"
          />
          <button
            onClick={handleExport}
            disabled={isLoading}
            className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-lg flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            {isLoading ? "Compiling Dossier..." : "Generate GDPR Dossier"}
          </button>
        </div>

        {exportData && (
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
            <div className="text-emerald-400 font-semibold flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" /> DSR Export Package Generated Successfully
            </div>
            <pre className="bg-slate-900 p-3 rounded text-[11px] text-slate-300 font-mono overflow-auto max-h-48">
              {JSON.stringify(exportData, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};
