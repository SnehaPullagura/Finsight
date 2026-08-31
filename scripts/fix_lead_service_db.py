with open("backend/app/services/lead.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("""class LeadService(BaseService[Lead, LeadRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(LeadRepository(db))
        self.rule_repo = LeadScoringRuleRepository(db)
        self.contact_repo = ContactRepository(db)
        self.company_repo = CompanyRepository(db)""", """class LeadService(BaseService[Lead, LeadRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(LeadRepository(db))
        self.db = db
        self.rule_repo = LeadScoringRuleRepository(db)
        self.contact_repo = ContactRepository(db)
        self.company_repo = CompanyRepository(db)""")

with open("backend/app/services/lead.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated LeadService.__init__ with self.db.")
