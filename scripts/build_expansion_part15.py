import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/security_governance/mfa_totp_authenticator.py
    write_file("backend/app/enterprise/security_governance/mfa_totp_authenticator.py", """import hmac
import hashlib
import time
import struct
import base64
from typing import Optional

class TOTPAuthenticator:
    @staticmethod
    def generate_current_totp(secret_base32: str, time_step: int = 30) -> str:
        # RFC 6238 Time-Based One-Time Password Implementation
        key = base64.b32decode(secret_base32, casefold=True)
        current_time = int(time.time())
        time_counter = current_time // time_step
        
        msg = struct.pack(">Q", time_counter)
        h = hmac.new(key, msg, hashlib.sha1).digest()
        
        offset = h[19] & 0x0F
        truncated_hash = (struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
        return f"{truncated_hash:06d}"

    @staticmethod
    def verify_totp_code(secret_base32: str, user_code: str, window: int = 1) -> bool:
        # Check current and adjacent time windows for clock drift
        current_time = int(time.time())
        for delta in range(-window, window + 1):
            key = base64.b32decode(secret_base32, casefold=True)
            time_counter = (current_time // 30) + delta
            msg = struct.pack(">Q", time_counter)
            h = hmac.new(key, msg, hashlib.sha1).digest()
            offset = h[19] & 0x0F
            truncated = (struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
            if f"{truncated:06d}" == str(user_code).strip():
                return True
        return False
""")

    # 2. backend/app/enterprise/security_governance/data_masking_engine.py
    write_file("backend/app/enterprise/security_governance/data_masking_engine.py", """import re
from typing import Any, Dict, List, Optional

class EnterpriseDataMaskingEngine:
    @staticmethod
    def mask_email(email: Optional[str]) -> str:
        if not email or "@" not in email:
            return "***@***.***"
        name_part, domain = email.split("@", 1)
        if len(name_part) <= 2:
            masked_name = name_part[0] + "*"
        else:
            masked_name = name_part[0] + ("*" * (len(name_part) - 2)) + name_part[-1]
        return f"{masked_name}@{domain}"

    @staticmethod
    def mask_phone(phone: Optional[str]) -> str:
        if not phone:
            return "***-***-****"
        digits = re.sub(r"\D", "", phone)
        if len(digits) >= 4:
            return f"***-***-{digits[-4:]}"
        return "***-***-****"
""")

    # 3. frontend/src/enterprise/EnterpriseSalesCompensationDashboard.tsx
    write_file("frontend/src/enterprise/EnterpriseSalesCompensationDashboard.tsx", """import React, { useState } from "react";
import { Award, TrendingUp, DollarSign, Target, CheckCircle2, ChevronRight } from "lucide-react";

export const EnterpriseSalesCompensationDashboard: React.FC = () => {
  const reps = [
    { name: "Alex Vance", quota: 250000, closed: 340000, attainment: "136.0%", commission: 42500, tier: "Tier 3 (2.0x)" },
    { name: "Sarah Connor", quota: 300000, closed: 315000, attainment: "105.0%", commission: 32250, tier: "Tier 2 (1.5x)" },
    { name: "John Wick", quota: 200000, closed: 180000, attainment: "90.0%", commission: 18000, tier: "Tier 1 (1.0x)" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            Sales Compensation & Commission Waterfall Dashboard
          </h3>
          <p className="text-xs text-slate-400">Real-time quota attainment tracking with automated multi-tier accelerator calculation</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Sales Representative</th>
              <th className="p-3 text-right">Quota Target</th>
              <th className="p-3 text-right">Closed Revenue</th>
              <th className="p-3 text-right">Attainment %</th>
              <th className="p-3">Active Accelerator</th>
              <th className="p-3 text-right text-emerald-400 font-bold">Commission Payout</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {reps.map((r, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-semibold">{r.name}</td>
                <td className="p-3 text-right text-slate-400">${r.quota.toLocaleString()}</td>
                <td className="p-3 text-right font-medium">${r.closed.toLocaleString()}</td>
                <td className="p-3 text-right text-emerald-400 font-bold">{r.attainment}</td>
                <td className="p-3"><span className="bg-slate-800 text-purple-300 px-2 py-0.5 rounded text-[11px] font-mono">{r.tier}</span></td>
                <td className="p-3 text-right font-bold text-emerald-400">${r.commission.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseAICopilotStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseAICopilotStudio.tsx", """import React, { useState } from "react";
import { Sparkles, Bot, Send, MessageSquare, CheckCircle2, RefreshCw } from "lucide-react";

export const EnterpriseAICopilotStudio: React.FC = () => {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I am ClientFlow AI Copilot. I can analyze your sales pipeline, predict quarterly finish, recommend pricing discounts, or draft contract renewal proposals. How can I assist you today?" }
  ]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            AI Copilot Studio & Natural Language Query Hub
          </h3>
          <p className="text-xs text-slate-400">Context-aware CRM generative assistant with multi-turn memory and action dispatch</p>
        </div>
      </div>

      <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 min-h-[300px] flex flex-col justify-between space-y-4">
        <div className="space-y-3">
          {messages.map((m, idx) => (
            <div key={idx} className={`flex items-start gap-3 ${m.role === "assistant" ? "text-slate-300" : "text-white"}`}>
              <div className="w-7 h-7 rounded-lg bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400 text-xs font-bold">
                AI
              </div>
              <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg text-xs leading-relaxed max-w-lg">
                {m.content}
              </div>
            </div>
          ))}
        </div>

        <div className="flex items-center gap-2 pt-2 border-t border-slate-800">
          <input
            type="text"
            placeholder="Ask AI Copilot: 'What is our expected quarter finish based on Monte Carlo simulation?'"
            className="flex-1 bg-slate-900 border border-slate-800 text-white px-3 py-2 rounded-lg text-xs focus:outline-none focus:border-emerald-500"
          />
          <button className="bg-emerald-600 hover:bg-emerald-500 text-white p-2 rounded-lg text-xs font-semibold shadow transition-colors">
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created TOTP authenticator, data masking, comp dashboard, and AI Copilot studio.")

if __name__ == '__main__':
    run()
