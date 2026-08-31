# ClientFlow CRM — Frontend Architecture

## 1. Technology Stack
- **Framework**: React 18 SPA (TypeScript 5.x)
- **Build Tool**: Vite 6 (Fast HMR & Optimized Bundles)
- **Styling**: Tailwind CSS v3 with custom Slate & Emerald enterprise color taxonomy
- **Icons**: Lucide React
- **HTTP Client**: Axios with automatic JWT refresh interceptor & tenant header injection
- **Routing**: React Router v6 with `ProtectedRoute` guards

## 2. Component Organization
```
frontend/src/
├── components/
│   ├── layout/       # AppLayout, Navbar, Sidebar
│   ├── common/       # GlobalSearchModal, DataTable, MetricCard
│   └── ai-assistant/ # AICopilotDrawer
├── context/          # AuthContext & TenantContext
├── pages/            # 16 domain pages (Dashboard, Contacts, Deals, etc.)
├── services/         # Typed API client wrapper
├── types/            # Complete TypeScript interfaces
├── App.tsx           # Route definitions
└── main.tsx          # Application entrypoint
```
