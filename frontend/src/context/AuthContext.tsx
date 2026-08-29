import React, { createContext, useContext, useState, useEffect } from "react";
import { User, Organization } from "../types";
import { api } from "../services/api";

interface AuthContextType {
  user: User | null;
  organization: Organization | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (tokens: { access_token: string; refresh_token: string; user: any; tenant_id?: string }) => void;
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
          setUser(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = (tokens: { access_token: string; refresh_token: string; user: any; tenant_id?: string }) => {
    localStorage.setItem("clientflow_access_token", tokens.access_token);
    localStorage.setItem("clientflow_refresh_token", tokens.refresh_token);
    if (tokens.tenant_id) {
      localStorage.setItem("clientflow_tenant_id", tokens.tenant_id);
    }
    setUser(tokens.user);
    api.getCurrentOrg()
      .then((orgRes) => setOrganization(orgRes.data))
      .catch(() => {});
  };

  const logout = () => {
    localStorage.removeItem("clientflow_access_token");
    localStorage.removeItem("clientflow_refresh_token");
    localStorage.removeItem("clientflow_tenant_id");
    setUser(null);
    setOrganization(null);
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
