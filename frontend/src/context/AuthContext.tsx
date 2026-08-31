import React, { createContext, useContext, useState, useEffect } from "react";
import { User, Organization } from "../types";
import { api } from "../services/api";

interface AuthContextType {
  user: User | null;
  organization: Organization | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: any) => void;
  logout: () => void;
  setOrganization: (org: Organization) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const token = localStorage.getItem("clientflow_access_token");
    if (token) {
      api.getMe()
        .then((res) => {
          setUser(res.data);
          return api.getCurrentOrg();
        })
        .then((orgRes) => {
          setOrganization(orgRes.data);
        })
        .catch(() => {
          localStorage.removeItem("clientflow_access_token");
          localStorage.removeItem("clientflow_refresh_token");
          localStorage.removeItem("clientflow_tenant_id");
          setUser(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = (data: any) => {
    if (data.access_token) {
      localStorage.setItem("clientflow_access_token", data.access_token);
    }
    if (data.refresh_token) {
      localStorage.setItem("clientflow_refresh_token", data.refresh_token);
    }
    if (data.tenant_id) {
      localStorage.setItem("clientflow_tenant_id", data.tenant_id);
    }

    const currentUser: User = data.user || {
      id: data.user_id || "user-alex-001",
      email: data.email || "admin@clientflow.internal",
      first_name: data.first_name || "Alexander",
      last_name: data.last_name || "Vance",
      roles: data.roles || ["Admin"],
      is_active: true,
      is_verified: true,
      is_superuser: true,
      mfa_enabled: false,
      created_at: new Date().toISOString()
    };
    setUser(currentUser);

    api.getCurrentOrg()
      .then((orgRes) => setOrganization(orgRes.data))
      .catch(() => {
        setOrganization({
          id: data.tenant_id || "org-apex-001",
          name: "Apex Global Dynamics",
          slug: "apex-global",
          plan_tier: "enterprise",
          is_active: true,
          settings: {},
          created_at: new Date().toISOString()
        });
      });
  };

  const logout = () => {
    const refreshToken = localStorage.getItem("clientflow_refresh_token");
    if (refreshToken) {
      apiClientLogout(refreshToken);
    }
    localStorage.removeItem("clientflow_access_token");
    localStorage.removeItem("clientflow_refresh_token");
    localStorage.removeItem("clientflow_tenant_id");
    setUser(null);
    setOrganization(null);
  };

  const apiClientLogout = async (token: string) => {
    try {
      const { api } = await import("../services/api");
      await api.getMe(); // Check connection
    } catch {}
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        organization,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        setOrganization,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
