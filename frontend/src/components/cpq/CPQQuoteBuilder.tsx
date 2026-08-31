import React, { useState } from "react";
import { Plus, Trash2, Calculator, ArrowRight, ShieldCheck, DollarSign } from "lucide-react";
import { api } from "../../services/api";

interface LineItem {
  id: string;
  product_id: string;
  name: string;
  unit_price: number;
  quantity: number;
  discount_percentage: number;
}

export const CPQQuoteBuilder: React.FC = () => {
  const [currency, setCurrency] = useState("USD");
  const [items, setItems] = useState<LineItem[]>([
    { id: "1", product_id: "prod-001", name: "Enterprise Cloud License", unit_price: 12000, quantity: 1, discount_percentage: 10 },
    { id: "2", product_id: "prod-002", name: "24/7 Priority Support SLA", unit_price: 3500, quantity: 1, discount_percentage: 0 }
  ]);
  const [calculation, setCalculation] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const addItem = () => {
    setItems([
      ...items,
      { id: Date.now().toString(), product_id: `prod-${Date.now()}`, name: "New Addon Service", unit_price: 1000, quantity: 1, discount_percentage: 0 }
    ]);
  };

  const removeItem = (id: string) => {
    setItems(items.filter(i => i.id !== id));
  };

  const updateItem = (id: string, field: keyof LineItem, val: any) => {
    setItems(items.map(i => i.id === id ? { ...i, [field]: val } : i));
  };

  const handleCalculate = async () => {
    setIsLoading(true);
    try {
      const payload = items.map(i => ({
        product_id: i.product_id,
        unit_price: Number(i.unit_price),
        quantity: Number(i.quantity),
        discount_percentage: Number(i.discount_percentage),
        tax_rate_pct: 5.0
      }));
      const res = await api.post("/cpq/calculate-pricing", payload, { params: { currency } });
      setCalculation(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            Configure Price & Quote (CPQ) Engine
          </h3>
          <p className="text-xs text-slate-400">Configure multi-currency line items, volume tiered discounts and tax calculations</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={currency}
            onChange={e => setCurrency(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded-lg px-3 py-1.5 focus:outline-none"
          >
            <option value="USD">USD ($)</option>
            <option value="EUR">EUR (€)</option>
            <option value="GBP">GBP (£)</option>
            <option value="CAD">CAD ($)</option>
            <option value="INR">INR (₹)</option>
          </select>
          <button
            onClick={addItem}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white rounded-lg border border-slate-700"
          >
            <Plus className="w-3.5 h-3.5 text-emerald-400" /> Add Item
          </button>
        </div>
      </div>

      <div className="space-y-3">
        {items.map((item, idx) => (
          <div key={item.id} className="grid grid-cols-12 gap-3 items-center bg-slate-950/60 p-3 rounded-lg border border-slate-800 text-xs">
            <div className="col-span-5">
              <input
                type="text"
                value={item.name}
                onChange={e => updateItem(item.id, "name", e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white"
                placeholder="Product or Service Name"
              />
            </div>
            <div className="col-span-2">
              <input
                type="number"
                value={item.unit_price}
                onChange={e => updateItem(item.id, "unit_price", Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white"
                placeholder="Unit Price"
              />
            </div>
            <div className="col-span-2">
              <input
                type="number"
                value={item.quantity}
                onChange={e => updateItem(item.id, "quantity", Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white"
                placeholder="Qty"
              />
            </div>
            <div className="col-span-2">
              <input
                type="number"
                value={item.discount_percentage}
                onChange={e => updateItem(item.id, "discount_percentage", Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white"
                placeholder="Disc %"
              />
            </div>
            <div className="col-span-1 flex justify-end">
              <button onClick={() => removeItem(item.id)} className="p-1.5 text-slate-500 hover:text-rose-400">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-slate-800">
        <button
          onClick={handleCalculate}
          disabled={isLoading}
          className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-lg flex items-center gap-2"
        >
          <Calculator className="w-4 h-4" />
          {isLoading ? "Computing Pricing..." : "Calculate Quote Pricing"}
        </button>

        {calculation && (
          <div className="flex items-center gap-6 text-xs">
            <div className="text-right">
              <div className="text-slate-400">Subtotal:</div>
              <div className="font-semibold text-white">{currency} {calculation.subtotal.toLocaleString()}</div>
            </div>
            <div className="text-right">
              <div className="text-rose-400">Discount:</div>
              <div className="font-semibold text-rose-400">-{currency} {calculation.total_discount.toLocaleString()}</div>
            </div>
            <div className="text-right">
              <div className="text-slate-400">Tax (5%):</div>
              <div className="font-semibold text-white">+{currency} {calculation.tax_amount.toLocaleString()}</div>
            </div>
            <div className="text-right pl-4 border-l border-slate-800">
              <div className="text-emerald-400 font-bold text-sm">Grand Total:</div>
              <div className="text-lg font-bold text-white">{currency} {calculation.total_amount.toLocaleString()}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
