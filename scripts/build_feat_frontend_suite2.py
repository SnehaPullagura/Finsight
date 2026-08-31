import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. frontend/src/components/integrations/DataImportWizard.tsx
    write_file("frontend/src/components/integrations/DataImportWizard.tsx", """import React, { useState } from "react";
import { UploadCloud, FileSpreadsheet, CheckCircle2, AlertCircle, ArrowRight } from "lucide-react";
import { api } from "../../services/api";

export const DataImportWizard: React.FC = () => {
  const [csvContent, setCsvContent] = useState("email,first_name,last_name,company\nsarah.connor@cyberdyne.internal,Sarah,Connor,Cyberdyne Systems\njohn.wick@continental.internal,John,Wick,The Continental");
  const [preview, setPreview] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handlePreview = async () => {
    setIsLoading(true);
    try {
      const res = await api.post("/integrations-hub/migrate-preview", {
        csv_content: csvContent,
        field_mappings: {
          email: "email",
          first_name: "first_name",
          last_name: "last_name",
          company: "company_name"
        }
      });
      setPreview(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div>
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <UploadCloud className="w-5 h-5 text-emerald-400" />
          Enterprise Data Import & Migration Wizard
        </h3>
        <p className="text-xs text-slate-400">Import and map CSV, HubSpot, or Salesforce contacts with live schema validation</p>
      </div>

      <div className="space-y-2">
        <label className="block text-xs font-semibold text-slate-300">Raw CSV Payload / File Content</label>
        <textarea
          rows={5}
          value={csvContent}
          onChange={e => setCsvContent(e.target.value)}
          className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-xs text-emerald-400 font-mono focus:outline-none focus:border-emerald-500"
        />
      </div>

      <button
        onClick={handlePreview}
        disabled={isLoading}
        className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-lg flex items-center gap-1.5"
      >
        <FileSpreadsheet className="w-4 h-4" />
        {isLoading ? "Validating Records..." : "Validate & Preview Migration"}
      </button>

      {preview && (
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
          <div className="flex items-center gap-6 text-xs border-b border-slate-800 pb-3">
            <div>Total Parsed: <span className="font-bold text-white">{preview.total_parsed}</span></div>
            <div className="text-emerald-400">Valid: <span className="font-bold">{preview.valid_count}</span></div>
            <div className="text-rose-400">Rejected: <span className="font-bold">{preview.rejected_count}</span></div>
          </div>
          <div className="space-y-1.5">
            <div className="text-[11px] font-semibold text-slate-400">Sample Validated Contacts:</div>
            {preview.sample_valid.map((c: any, idx: number) => (
              <div key={idx} className="flex items-center gap-2 text-xs text-slate-300">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>{c.first_name} {c.last_name} ({c.email}) — <strong className="text-slate-400">{c.company_name}</strong></span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
""")

    # 2. frontend/src/pages/cpq/CPQPage.tsx
    write_file("frontend/src/pages/cpq/CPQPage.tsx", """import React from "react";
import { CPQQuoteBuilder } from "../../components/cpq/CPQQuoteBuilder";

export const CPQPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <CPQQuoteBuilder />
    </div>
  );
};
""")

    # 3. frontend/src/pages/analytics/AdvancedAnalyticsPage.tsx
    write_file("frontend/src/pages/analytics/AdvancedAnalyticsPage.tsx", """import React from "react";
import { ForecastSimulator } from "../../components/analytics/ForecastSimulator";

export const AdvancedAnalyticsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <ForecastSimulator />
    </div>
  );
};
""")

    # 4. frontend/src/pages/integrations/IntegrationsPage.tsx
    write_file("frontend/src/pages/integrations/IntegrationsPage.tsx", """import React from "react";
import { DataImportWizard } from "../../components/integrations/DataImportWizard";

export const IntegrationsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <DataImportWizard />
    </div>
  );
};
""")

    # 5. frontend/src/pages/governance/GovernancePage.tsx
    write_file("frontend/src/pages/governance/GovernancePage.tsx", """import React, { useState } from "react";
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
""")

    print("Created remaining frontend components and pages.")

if __name__ == '__main__':
    run()
