import React, { useState } from "react";
import { Shield, Key, Lock, CheckCircle2 } from "lucide-react";

export const EnterpriseSAMLExecutiveStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Shield className="w-5 h-5 text-emerald-400" />
            SAML 2.0 & Okta Enterprise SSO Configuration
          </h3>
          <p className="text-xs text-slate-400">Identity Provider (IdP) single sign-on metadata and SCIM 2.0 user provisioning</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          SSO Enforced
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">IdP Issuer URL</span>
          <div className="text-xs font-mono text-white truncate">https://auth.okta.internal</div>
          <span className="text-[10px] text-emerald-400">Connected</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Assertion Signature</span>
          <div className="text-xs font-mono text-white">SHA-256 RSA</div>
          <span className="text-[10px] text-emerald-400">Verified</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">SCIM User Sync</span>
          <div className="text-xs font-mono text-white">Real-Time</div>
          <span className="text-[10px] text-emerald-400">Active (450 Users)</span>
        </div>
      </div>
    </div>
  );
};
