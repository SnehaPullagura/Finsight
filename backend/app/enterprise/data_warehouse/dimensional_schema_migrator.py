from typing import Any, Dict, List

class DimensionalSchemaMigrator:
    @staticmethod
    def get_ddl_statements() -> List[str]:
        return [
            """
            CREATE TABLE IF NOT EXISTS dim_company (
                company_key VARCHAR(64) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                industry VARCHAR(100),
                tier VARCHAR(50),
                annual_revenue NUMERIC(15, 2),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS dim_contact (
                contact_key VARCHAR(64) PRIMARY KEY,
                company_key VARCHAR(64) REFERENCES dim_company(company_key),
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(255) UNIQUE,
                lifecycle_stage VARCHAR(50)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS fact_deal_snapshot (
                deal_key VARCHAR(64) PRIMARY KEY,
                company_key VARCHAR(64) REFERENCES dim_company(company_key),
                contact_key VARCHAR(64) REFERENCES dim_contact(contact_key),
                deal_amount NUMERIC(15, 2) NOT NULL,
                probability NUMERIC(5, 2),
                stage VARCHAR(100),
                is_won BOOLEAN DEFAULT FALSE,
                is_lost BOOLEAN DEFAULT FALSE,
                snapshot_date DATE NOT NULL
            );
            """
        ]
