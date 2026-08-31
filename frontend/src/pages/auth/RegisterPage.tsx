import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Zap } from "lucide-react";
import { api } from "../../services/api";
import { useAuth } from "../../context/AuthContext";

export const RegisterPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [orgName, setOrgName] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    try {
      await api.register({
        email,
        password,
        first_name: firstName,
        last_name: lastName,
        organization_name: orgName
      });
      const res = await api.login({ email, password });
      login(res.data);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || "Failed to create account.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="w-12 h-12 rounded-2xl bg-emerald-500 text-slate-950 mx-auto flex items-center justify-center font-bold shadow-lg shadow-emerald-500/25 mb-4">
          <Zap className="w-7 h-7 fill-current" />
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-white">Create Organization Account</h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4">
        <div className="bg-slate-900 py-8 px-6 shadow-2xl rounded-2xl border border-slate-800">
          {error && <div className="mb-4 p-3 bg-rose-500/10 text-rose-400 text-xs rounded-lg">{error}</div>}
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="grid grid-cols-2 gap-2">
              <input required placeholder="First Name" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-xs text-white" value={firstName} onChange={e => setFirstName(e.target.value)} />
              <input required placeholder="Last Name" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-xs text-white" value={lastName} onChange={e => setLastName(e.target.value)} />
            </div>
            <input required placeholder="Organization Name" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-xs text-white" value={orgName} onChange={e => setOrgName(e.target.value)} />
            <input type="email" required placeholder="Email Address" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-xs text-white" value={email} onChange={e => setEmail(e.target.value)} />
            <input type="password" required minLength={8} placeholder="Password" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-xs text-white" value={password} onChange={e => setPassword(e.target.value)} />
            <button type="submit" disabled={isLoading} className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-xs rounded-lg">
              {isLoading ? "Setting up workspace..." : "Register Organization"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
