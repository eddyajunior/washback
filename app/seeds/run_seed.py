from app.infrastructure.database.database import SessionLocal
from app.seeds.seed import create_campaigns, create_customers, create_washes


db = SessionLocal()

customers = create_customers(db)
create_washes(db, customers)
create_campaigns(db, customers)

db.close()