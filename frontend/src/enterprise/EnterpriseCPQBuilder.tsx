import React, { useState } from "react";
import { Calculator, Plus, Trash2, ShieldCheck, Check, DollarSign } from "lucide-react";

interface LineItem {
  id: string;
  name: string;
  unitPrice: number;
  quantity: number;
  discountPct: number;
}

export const EnterpriseCPQBuilder: React.FC = () => {
  const [items, setItems] = useState<LineItem[]>([
    { id: "1", name: "Enterprise CRM Seat License", unitPrice: 120, quantity: 50, discountPct: 10 },
    { id: "2", name: "White-Glove Implementation Package", unitPrice: 15000, quantity: 1, discountPct: 0 }
  ]);

  const subtotal = items.reduce((sum, item) => sum + (item.unitPrice * item.quantity), 0);
  const discountTotal = items.reduce((sum, item) => sum + (item.unitPrice * item.quantity * (item.discountPct / 100)), 0);
  const finalTotal = subtotal - discountTotal;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            CPQ Enterprise Quote Generator & Pricing Engine
          </h3>
          <p className="text-xs text-slate-400">Configure complex multi-line quotes with volume discount matrices and margin guardrails</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Product / Service</th>
              <th className="p-3 text-right">Unit Price</th>
              <th className="p-3 text-right">Quantity</th>
              <th className="p-3 text-right">Discount %</th>
              <th className="p-3 text-right">Line Total</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {items.map(item => {
              const lineTotal = (item.unitPrice * item.quantity) * (1 - item.discountPct / 100);
              return (
                <tr key={item.id} className="hover:bg-slate-800/30">
                  <td className="p-3 font-medium">{item.name}</td>
                  <td className="p-3 text-right">${item.unitPrice.toLocaleString()}</td>
                  <td className="p-3 text-right">{item.quantity}</td>
                  <td className="p-3 text-right text-amber-400">{item.discountPct}%</td>
                  <td className="p-3 text-right font-bold text-emerald-400">${lineTotal.toLocaleString()}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="flex justify-end pt-4 border-t border-slate-800">
        <div className="w-64 space-y-2 text-xs">
          <div className="flex justify-between text-slate-400">
            <span>List Price Subtotal:</span>
            <span className="font-semibold text-white">${subtotal.toLocaleString()}</span>
          </div>
          <div className="flex justify-between text-slate-400">
            <span>Volume Discount:</span>
            <span className="font-semibold text-amber-400">-${discountTotal.toLocaleString()}</span>
          </div>
          <div className="flex justify-between text-sm font-bold text-white pt-2 border-t border-slate-800">
            <span>Payable Amount:</span>
            <span className="text-emerald-400">${finalTotal.toLocaleString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
