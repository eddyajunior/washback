from app.infrastructure.database.models.company import Company

class CompanyRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, company: Company):
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company