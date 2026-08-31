with open("frontend/src/App.tsx", "r", encoding="utf-8") as f:
    content = f.read()

import_lines = """import { CPQPage } from "./pages/cpq/CPQPage";
import { AdvancedAnalyticsPage } from "./pages/analytics/AdvancedAnalyticsPage";
import { IntegrationsPage } from "./pages/integrations/IntegrationsPage";
import { GovernancePage } from "./pages/governance/GovernancePage";
"""
content = import_lines + content
content = content.replace(
    """            <Route path="settings" element={<SettingsPage />} />""",
    """            <Route path="cpq" element={<CPQPage />} />
            <Route path="advanced-analytics" element={<AdvancedAnalyticsPage />} />
            <Route path="integrations" element={<IntegrationsPage />} />
            <Route path="governance" element={<GovernancePage />} />
            <Route path="settings" element={<SettingsPage />} />"""
)

with open("frontend/src/App.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated App.tsx with CPQ, Analytics, Integrations, and Governance routes.")
