import React, { useEffect, useState } from "react";
import { Folder, FileText, Download } from "lucide-react";
import { api } from "../../services/api";
import { Document } from "../../types";

export const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);

  useEffect(() => {
    api.getProducts().then(() => {
      setDocuments([
        { id: "1", tenant_id: "org-1", name: "Enterprise_SLA_Agreement_2026.pdf", file_size_bytes: 2450000, mime_type: "application/pdf", is_public: false, download_count: 14, tags: ["legal", "sla"], created_at: new Date().toISOString() },
        { id: "2", tenant_id: "org-1", name: "Security_Compliance_SOC2.pdf", file_size_bytes: 4800000, mime_type: "application/pdf", is_public: true, download_count: 42, tags: ["security"], created_at: new Date().toISOString() }
      ]);
    }).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Document Vault</h1>
        <p className="text-xs text-slate-500">Secure assets, contracts, proposals, and version-controlled files</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {documents.map(d => (
          <div key={d.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-2">
            <div className="flex items-center gap-3">
              <FileText className="w-6 h-6 text-emerald-600" />
              <div>
                <h4 className="text-xs font-bold text-slate-900 line-clamp-1">{d.name}</h4>
                <span className="text-[10px] text-slate-400">{(d.file_size_bytes / 1024 / 1024).toFixed(2)} MB • {d.download_count} downloads</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
