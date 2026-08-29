import React, { useEffect, useState } from "react";
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
