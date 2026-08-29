import React, { useEffect, useState } from "react";
import { Megaphone, Play } from "lucide-react";
import { api } from "../../services/api";
import { Campaign } from "../../types";

export const CampaignsPage: React.FC = () => {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);

  useEffect(() => {
    api.getCampaigns().then(res => setCampaigns(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Marketing Campaigns</h1>
        <p className="text-xs text-slate-500">Audience segmentation, email/SMS broadcasts, and attribution</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {campaigns.map(c => (
          <div key={c.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-2">
            <h4 className="text-xs font-bold text-slate-900">{c.name}</h4>
            <div className="text-[11px] text-slate-500">{c.sent_count} sent • {c.open_count} opened • {c.conversion_count} converted</div>
          </div>
        ))}
        {campaigns.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">No campaigns launched.</div>}
      </div>
    </div>
  );
};
