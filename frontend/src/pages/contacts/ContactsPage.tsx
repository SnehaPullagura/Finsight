import React, { useEffect, useState } from "react";
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
