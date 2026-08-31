import React, { useState } from "react";
import { Mail, Send, Eye, Sparkles, Code } from "lucide-react";

export const EmailTemplateComposer: React.FC = () => {
  const [subject, setSubject] = useState("Exciting Updates regarding {{company.name}} & ClientFlow");
  const [body, setBody] = useState("Hi {{contact.first_name}},\n\nThank you for exploring ClientFlow CRM! We've prepared your custom pricing proposal for {{deal.value}}.\n\nBest regards,\n{{user.name}}");
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
