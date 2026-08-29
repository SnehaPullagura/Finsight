import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    write_file("frontend/src/pages/activities/TimelinePage.tsx", """import React, { useEffect, useState } from "react";
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
""")

    write_file("frontend/src/pages/tasks/TasksPage.tsx", """import React, { useEffect, useState } from "react";
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
""")

    write_file("frontend/src/pages/calendar/CalendarPage.tsx", """import React, { useEffect, useState } from "react";
import { Calendar as CalendarIcon, Clock, MapPin } from "lucide-react";
import { api } from "../../services/api";
import { CalendarEvent } from "../../types";

export const CalendarPage: React.FC = () => {
  const [events, setEvents] = useState<CalendarEvent[]>([]);

  useEffect(() => {
    api.getCalendarEvents().then(res => setEvents(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Meeting Calendar</h1>
        <p className="text-xs text-slate-500">Upcoming client engagements, demos, and syncs</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {events.map(ev => (
          <div key={ev.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-2">
            <h4 className="text-xs font-bold text-slate-900">{ev.title}</h4>
            <div className="text-[11px] text-slate-500 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5" />
              <span>{new Date(ev.start_time).toLocaleString()}</span>
            </div>
            {ev.location && (
              <div className="text-[11px] text-slate-500 flex items-center gap-1.5">
                <MapPin className="w-3.5 h-3.5" />
                <span>{ev.location}</span>
              </div>
            )}
          </div>
        ))}
        {events.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">No scheduled meetings today.</div>}
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/communications/CommunicationsPage.tsx", """import React, { useState } from "react";
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
""")

    write_file("frontend/src/pages/documents/DocumentsPage.tsx", """import React, { useEffect, useState } from "react";
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
""")

    write_file("frontend/src/pages/products/ProductsPage.tsx", """import React, { useEffect, useState } from "react";
import { Plus, Package } from "lucide-react";
import { api } from "../../services/api";
import { Product } from "../../types";

export const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    api.getProducts().then(res => setProducts(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Products & Services Catalog</h1>
        <p className="text-xs text-slate-500">Tiered pricing, SKU management, and tax rates</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {products.map(p => (
          <div key={p.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-2">
            <div className="flex justify-between items-start">
              <h4 className="text-xs font-bold text-slate-900">{p.name}</h4>
              <span className="text-xs font-bold text-emerald-600">${Number(p.unit_price).toLocaleString()}</span>
            </div>
            <div className="text-[11px] text-slate-400">SKU: {p.sku}</div>
          </div>
        ))}
        {products.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">Catalog is ready for product entries.</div>}
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/proposals/ProposalsPage.tsx", """import React, { useEffect, useState } from "react";
import { FileCheck, CheckCircle2 } from "lucide-react";
import { api } from "../../services/api";
import { Proposal } from "../../types";

export const ProposalsPage: React.FC = () => {
  const [proposals, setProposals] = useState<Proposal[]>([]);

  useEffect(() => {
    api.getProposals().then(res => setProposals(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Proposals & SOWs</h1>
        <p className="text-xs text-slate-500">Interactive proposals, line items, and customer acceptance</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-600 font-semibold border-b">
            <tr>
              <th className="p-3.5">Proposal #</th>
              <th className="p-3.5">Title</th>
              <th className="p-3.5">Total Value</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {proposals.map(p => (
              <tr key={p.id} className="hover:bg-slate-50">
                <td className="p-3.5 font-semibold text-slate-900">{p.proposal_number}</td>
                <td className="p-3.5">{p.title}</td>
                <td className="p-3.5 font-bold text-emerald-600">${Number(p.total_amount).toLocaleString()}</td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800 uppercase">{p.status}</span>
                </td>
              </tr>
            ))}
            {proposals.length === 0 && <tr><td colSpan={4} className="p-8 text-center text-slate-400">No proposals generated yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/quotes/QuotesPage.tsx", """import React, { useEffect, useState } from "react";
import { FileSpreadsheet } from "lucide-react";
import { api } from "../../services/api";
import { Quote } from "../../types";

export const QuotesPage: React.FC = () => {
  const [quotes, setQuotes] = useState<Quote[]>([]);

  useEffect(() => {
    api.getQuotes().then(res => setQuotes(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Quotes</h1>
        <p className="text-xs text-slate-500">Formal sales quotes and revision approvals</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {quotes.map(q => (
          <div key={q.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-2">
            <h4 className="text-xs font-bold text-slate-900">{q.quote_number}</h4>
            <div className="text-xs font-bold text-emerald-600">${Number(q.total_amount).toLocaleString()}</div>
          </div>
        ))}
        {quotes.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">No active quotes.</div>}
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/invoices/InvoicesPage.tsx", """import React, { useEffect, useState } from "react";
import { Receipt } from "lucide-react";
import { api } from "../../services/api";
import { Invoice } from "../../types";

export const InvoicesPage: React.FC = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);

  useEffect(() => {
    api.getInvoices().then(res => setInvoices(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Invoices & Billing</h1>
        <p className="text-xs text-slate-500">Payment statuses, due dates, and accounting records</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-600 font-semibold border-b">
            <tr>
              <th className="p-3.5">Invoice #</th>
              <th className="p-3.5">Due Date</th>
              <th className="p-3.5">Total Amount</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {invoices.map(i => (
              <tr key={i.id} className="hover:bg-slate-50">
                <td className="p-3.5 font-semibold text-slate-900">{i.invoice_number}</td>
                <td className="p-3.5 text-slate-500">{i.due_date}</td>
                <td className="p-3.5 font-bold text-slate-900">${Number(i.total_amount).toLocaleString()}</td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800 uppercase">{i.payment_status}</span>
                </td>
              </tr>
            ))}
            {invoices.length === 0 && <tr><td colSpan={4} className="p-8 text-center text-slate-400">No invoices generated yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    print("Part D1 generated.")

if __name__ == '__main__':
    run()
