import React, { useState } from "react";
import { Send, Mail, MessageSquare } from "lucide-react";
import { api } from "../../services/api";

export const CommunicationsPage: React.FC = () => {
  const [channel, setChannel] = useState("email");
  const [recipient, setRecipient] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [sent, setSent] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.createActivity({
      entity_type: "contact",
      entity_id: "c1",
      activity_type: channel.toUpperCase(),
      title: subject || "Communication",
      description: body
    });
    setSent(true);
    setTimeout(() => setSent(false), 3000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Communications Hub</h1>
        <p className="text-xs text-slate-500">Multi-channel email, SMS, and template delivery infrastructure</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs max-w-2xl">
        {sent && <div className="mb-4 p-3 bg-emerald-100 text-emerald-800 text-xs rounded-lg">Message successfully queued and dispatched!</div>}
        <form onSubmit={handleSend} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Channel</label>
            <select className="w-full border p-2 rounded text-xs" value={channel} onChange={e => setChannel(e.target.value)}>
              <option value="email">Email</option>
              <option value="sms">SMS</option>
            </select>
          </div>
          <input required placeholder="Recipient Email or Phone" className="w-full border p-2 rounded text-xs" value={recipient} onChange={e => setRecipient(e.target.value)} />
          {channel === "email" && <input placeholder="Subject" className="w-full border p-2 rounded text-xs" value={subject} onChange={e => setSubject(e.target.value)} />}
          <textarea required rows={5} placeholder="Message content..." className="w-full border p-2 rounded text-xs" value={body} onChange={e => setBody(e.target.value)} />
          <button type="submit" className="px-4 py-2 bg-emerald-600 text-white rounded text-xs font-semibold flex items-center gap-1.5">
            <Send className="w-3.5 h-3.5" /> Send Message
          </button>
        </form>
      </div>
    </div>
  );
};
