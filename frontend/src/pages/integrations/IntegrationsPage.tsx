import React from "react";
import { DataImportWizard } from "../../components/integrations/DataImportWizard";

export const IntegrationsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <DataImportWizard />
    </div>
  );
};
