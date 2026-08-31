from typing import Any, Dict, List

class EnterpriseMigrationTemplates:
    @staticmethod
    def get_crm_mapping_templates() -> Dict[str, Dict[str, str]]:
        return {
            "salesforce": {
                "AccountId": "company_id",
                "AccountName": "company_name",
                "ContactEmail": "email",
                "FirstName": "first_name",
                "LastName": "last_name",
                "Phone": "phone",
                "OpportunityAmount": "deal_value",
                "StageName": "stage",
                "CloseDate": "expected_close_date",
                "LeadSource": "lead_source",
                "AnnualRevenue": "annual_revenue"
            },
            "hubspot": {
                "hs_object_id": "external_id",
                "email": "email",
                "firstname": "first_name",
                "lastname": "last_name",
                "phone": "phone",
                "company": "company_name",
                "amount": "deal_value",
                "dealstage": "stage",
                "closedate": "expected_close_date",
                "lifecyclestage": "lifecycle_stage"
            },
            "zoho": {
                "Account_Name": "company_name",
                "Email": "email",
                "First_Name": "first_name",
                "Last_Name": "last_name",
                "Phone": "phone",
                "Amount": "deal_value",
                "Stage": "stage",
                "Closing_Date": "expected_close_date",
                "Lead_Source": "lead_source"
            }
        }
