import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    write_file("frontend/src/pages/contacts/ContactsPage.tsx", """import React, { useEffect, useState } from "react";
import { Plus, Search } from "lucide-react";
import { api } from "../../services/api";
import { Contact } from "../../types";

export const ContactsPage: React.FC = () => {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [search, setSearch] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [newContact, setNewContact] = useState({ first_name: "", last_name: "", email: "", phone: "", title: "", lifecycle_stage: "lead" });

  useEffect(() => { loadContacts(); }, []);
  const loadContacts = () => { api.getContacts().then(res => setContacts(res.data)).catch(console.error); };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.createContact(newContact);
    setShowModal(false);
    setNewContact({ first_name: "", last_name: "", email: "", phone: "", title: "", lifecycle_stage: "lead" });
    loadContacts();
  };

  const filtered = contacts.filter(c => `${c.first_name} ${c.last_name}`.toLowerCase().includes(search.toLowerCase()) || c.email.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-slate-900">Contacts</h1>
          <p className="text-xs text-slate-500">Manage individuals, relationships, and stakeholder profiles</p>
        </div>
        <button onClick={() => setShowModal(true)} className="flex items-center gap-1.5 px-3 py-2 bg-emerald-600 text-white rounded-lg text-xs font-semibold">
          <Plus className="w-4 h-4" /> Add Contact
        </button>
      </div>

      <div className="flex items-center gap-3 bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
        <Search className="w-4 h-4 text-slate-400" />
        <input placeholder="Filter contacts..." className="flex-1 text-xs outline-none" value={search} onChange={e => setSearch(e.target.value)} />
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
              <th className="p-3.5">Name</th>
              <th className="p-3.5">Email</th>
              <th className="p-3.5">Phone</th>
              <th className="p-3.5">Title</th>
              <th className="p-3.5">Lifecycle Stage</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {filtered.map(c => (
              <tr key={c.id} className="hover:bg-slate-50">
                <td className="p-3.5 font-semibold text-slate-900">{c.first_name} {c.last_name}</td>
                <td className="p-3.5 text-slate-600">{c.email}</td>
                <td className="p-3.5 text-slate-500">{c.phone || "—"}</td>
                <td className="p-3.5 text-slate-500">{c.title || "—"}</td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100 text-emerald-800 uppercase">
                    {c.lifecycle_stage}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl border border-slate-200">
            <h3 className="text-sm font-bold text-slate-900 mb-4">Create New Contact</h3>
            <form onSubmit={handleCreate} className="space-y-3">
              <div className="grid grid-cols-2 gap-2">
                <input required placeholder="First Name" className="border p-2 rounded text-xs" value={newContact.first_name} onChange={e => setNewContact({...newContact, first_name: e.target.value})} />
                <input required placeholder="Last Name" className="border p-2 rounded text-xs" value={newContact.last_name} onChange={e => setNewContact({...newContact, last_name: e.target.value})} />
              </div>
              <input required type="email" placeholder="Email Address" className="w-full border p-2 rounded text-xs" value={newContact.email} onChange={e => setNewContact({...newContact, email: e.target.value})} />
              <input placeholder="Phone Number" className="w-full border p-2 rounded text-xs" value={newContact.phone} onChange={e => setNewContact({...newContact, phone: e.target.value})} />
              <input placeholder="Job Title" className="w-full border p-2 rounded text-xs" value={newContact.title} onChange={e => setNewContact({...newContact, title: e.target.value})} />
              <div className="flex justify-end gap-2 pt-2">
                <button type="button" onClick={() => setShowModal(false)} className="px-3 py-1.5 border rounded text-xs text-slate-600">Cancel</button>
                <button type="submit" className="px-3 py-1.5 bg-emerald-600 text-white rounded text-xs font-semibold">Save Contact</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
""")

    write_file("frontend/src/pages/companies/CompaniesPage.tsx", """import React, { useEffect, useState } from "react";
import { Plus, Search, Building2 } from "lucide-react";
import { api } from "../../services/api";
import { Company } from "../../types";

export const CompaniesPage: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    api.getCompanies().then(res => setCompanies(res.data)).catch(console.error);
  }, []);

  const filtered = companies.filter(c => c.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Companies & Accounts</h1>
        <p className="text-xs text-slate-500">Corporate entities, parent-subsidiary hierarchies, and annual valuations</p>
      </div>

      <div className="flex items-center gap-3 bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
        <Search className="w-4 h-4 text-slate-400" />
        <input placeholder="Filter companies..." className="flex-1 text-xs outline-none" value={search} onChange={e => setSearch(e.target.value)} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map(c => (
          <div key={c.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-lg bg-purple-50 text-purple-600 border border-purple-100">
                <Building2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900">{c.name}</h3>
                <span className="text-[11px] text-slate-400">{c.domain || "no-domain.com"}</span>
              </div>
            </div>
            <div className="text-xs text-slate-600 space-y-1 pt-2 border-t border-slate-100">
              <div className="flex justify-between">
                <span className="text-slate-400">Industry:</span>
                <span className="font-semibold text-slate-700 capitalize">{c.industry || "General"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Annual Revenue:</span>
                <span className="font-semibold text-emerald-600">${Number(c.annual_revenue || 0).toLocaleString()}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/leads/LeadsPage.tsx", """import React, { useEffect, useState } from "react";
import { CheckCircle2 } from "lucide-react";
import { api } from "../../services/api";
import { Lead } from "../../types";

export const LeadsPage: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);

  useEffect(() => { loadLeads(); }, []);
  const loadLeads = () => { api.getLeads().then(res => setLeads(res.data)).catch(console.error); };

  const handleConvert = async (leadId: string) => {
    await api.convertLead(leadId, { create_deal: true });
    loadLeads();
  };

  const handleQualify = async (leadId: string) => {
    await api.qualifyLead(leadId);
    loadLeads();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Leads & Scoring</h1>
        <p className="text-xs text-slate-500">Configurable multi-criteria lead qualification and 1-click deal conversion</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
              <th className="p-3.5">Lead Name</th>
              <th className="p-3.5">Company</th>
              <th className="p-3.5">Score & Grade</th>
              <th className="p-3.5">Status</th>
              <th className="p-3.5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {leads.map(l => (
              <tr key={l.id} className="hover:bg-slate-50">
                <td className="p-3.5">
                  <div className="font-semibold text-slate-900">{l.first_name} {l.last_name}</div>
                  <div className="text-slate-400 text-[11px]">{l.email}</div>
                </td>
                <td className="p-3.5 font-medium text-slate-800">{l.company_name || "Independent"}</td>
                <td className="p-3.5">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
                    Grade {l.qualification_grade} ({l.score}/100)
                  </span>
                </td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700 uppercase">
                    {l.status}
                  </span>
                </td>
                <td className="p-3.5 text-right space-x-2">
                  {l.status !== "converted" ? (
                    <>
                      <button onClick={() => handleQualify(l.id)} className="px-2.5 py-1 bg-slate-100 text-slate-700 rounded text-xs font-semibold">Recalculate</button>
                      <button onClick={() => handleConvert(l.id)} className="px-2.5 py-1 bg-emerald-600 text-white rounded text-xs font-semibold">1-Click Convert ➔</button>
                    </>
                  ) : (
                    <span className="text-emerald-600 font-semibold text-xs inline-flex items-center gap-1">
                      <CheckCircle2 className="w-4 h-4" /> Converted
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/deals/DealsKanbanPage.tsx", """import React, { useEffect, useState } from "react";
import { ChevronRight } from "lucide-react";
import { api } from "../../services/api";
import { KanbanBoard } from "../../types";

export const DealsKanbanPage: React.FC = () => {
  const [board, setBoard] = useState<KanbanBoard | null>(null);

  useEffect(() => { loadBoard(); }, []);
  const loadBoard = () => { api.getKanbanBoard().then(res => setBoard(res.data)).catch(console.error); };

  const handleStageMove = async (dealId: string, targetStageId: string) => {
    await api.transitionDealStage(dealId, { stage_id: targetStageId });
    loadBoard();
  };

  if (!board) return <div className="p-8 text-center text-sm text-slate-500">Loading sales pipelines...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">{board.pipeline_name}</h1>
        <p className="text-xs text-slate-500">Advance deals across validated sales stages</p>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-4">
        {board.columns.map((col, idx) => (
          <div key={col.stage_id} className="w-80 shrink-0 bg-slate-100/70 rounded-xl p-3 border border-slate-200/80 flex flex-col max-h-[75vh]">
            <div className="flex items-center justify-between mb-3 px-1">
              <div>
                <h4 className="text-xs font-bold text-slate-800">{col.stage_name}</h4>
                <div className="text-[10px] text-slate-400">{col.deal_count} deals • ${col.total_value.toLocaleString()}</div>
              </div>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-white text-slate-600 border border-slate-200">
                {col.probability}%
              </span>
            </div>

            <div className="flex-1 overflow-y-auto space-y-2 pr-1">
              {col.deals.map(d => (
                <div key={d.id} className="bg-white p-3.5 rounded-lg border border-slate-200 shadow-2xs space-y-2">
                  <div className="flex justify-between items-start">
                    <h5 className="text-xs font-bold text-slate-900">{d.name}</h5>
                    <span className="text-xs font-bold text-emerald-600">${Number(d.value).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] text-slate-400 pt-2 border-t border-slate-100">
                    <span>{d.probability}% Prob.</span>
                    {idx < board.columns.length - 1 && (
                      <button
                        onClick={() => handleStageMove(d.id, board.columns[idx + 1].stage_id)}
                        className="px-2 py-0.5 bg-slate-50 hover:bg-emerald-50 text-slate-600 rounded border border-slate-200 text-[10px] font-medium flex items-center gap-0.5"
                      >
                        Advance <ChevronRight className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Part C2 generated.")

if __name__ == '__main__':
    run()
