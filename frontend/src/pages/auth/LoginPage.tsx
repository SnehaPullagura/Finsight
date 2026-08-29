import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Zap, Lock, Mail, ArrowRight, ShieldCheck } from "lucide-react";
import { api } from "../../services/api";
import { useAuth } from "../../context/AuthContext";

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("admin@clientflow.internal");
  const [password, setPassword] = useState("AdminSecret123!");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);
    try {
      const res = await api.login({ email, password });
      login(res.data);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || "Invalid credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setEmail("admin@clientflow.internal");
    setPassword("AdminSecret123!");
    setIsLoading(true);
    try {
      const res = await api.login({ email: "admin@clientflow.internal", password: "AdminSecret123!" });
      login(res.data);
      navigate("/dashboard");
    } catch (err) {
      try {
        await api.register({
          email: "admin@clientflow.internal",
          password: "AdminSecret123!",
          first_name: "Alexander",
          last_name: "Vance",
          organization_name: "Apex Global Dynamics"
        });
        const res = await api.login({ email: "admin@clientflow.internal", password: "AdminSecret123!" });
        login(res.data);
        navigate("/dashboard");
      } catch (regErr: any) {
        setError("Unable to authenticate demo user.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10 text-center">
        <div className="w-12 h-12 rounded-2xl bg-emerald-500 text-slate-950 mx-auto flex items-center justify-center font-bold shadow-lg shadow-emerald-500/25 mb-4">
          <Zap className="w-7 h-7 fill-current" />
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-white">ClientFlow CRM</h2>
        <p className="mt-1 text-xs text-slate-400">Enterprise High-Velocity CRM & Operations</p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10 px-4">
        <div className="bg-slate-900/90 py-8 px-6 shadow-2xl rounded-2xl border border-slate-800">
          {error && <div className="mb-4 p-3 rounded-lg bg-rose-500/10 text-rose-400 text-xs">{error}</div>}
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-medium text-slate-300">Corporate Email</label>
              <input type="email" required className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-white" value={email} onChange={e => setEmail(e.target.value)} />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300">Password</label>
              <input type="password" required className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-white" value={password} onChange={e => setPassword(e.target.value)} />
            </div>
            <button type="submit" disabled={isLoading} className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-xs rounded-lg">
              {isLoading ? "Authenticating..." : "Sign In to Platform"}
            </button>
          </form>
          <div className="mt-4 pt-4 border-t border-slate-800">
            <button type="button" onClick={handleDemoLogin} className="w-full py-2 bg-slate-800 text-emerald-400 font-medium text-xs rounded-lg border border-slate-700">
              ⚡ Quick Demo 1-Click Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
