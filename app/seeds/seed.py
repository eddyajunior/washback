import random

from faker import Faker
from datetime import datetime, timedelta

from app.infrastructure.database.database import SessionLocal

from app.infrastructure.database.models.campaign import Campaign
from app.infrastructure.database.models.company import Company
from app.infrastructure.database.models.customer import Customer
from app.infrastructure.database.models.wash import Wash


fake = Faker("pt_BR")
db = SessionLocal()

# Criar empersa principal
company = Company(name="Lava Rápido IA")
db.add(company)
db.commit()
db.refresh(company)


WASH_TYPES = [
    "Lavagem Simples",
    "Lavagem Completa",
    "Lavagem Premium",
    "Higienização",
    "Polimento"
]


def create_customers(total=50):
    customers_created = []

    for _ in range(total):

        customer = Customer(
            name=fake.name(),
            phone=fake.phone_number(),
            car_plate=fake.license_plate(),
            company_id=company.id,
            car_model=f"{fake.company()} {fake.word().capitalize()}"
        )

        db.add(customer)

        customers_created.append(customer)

    db.commit()

    for c in customers_created:
        db.refresh(c)

    return customers_created


def create_washes(customers):
    wash_type= [
        "Lavagem Simples",
        "Lavagem Completa",
        "Polimento",
        "Higienização"
        ]

    washes = [] 

    for customer in customers:
        for _ in range(random.randint(2, 8)):
            wash = Wash(
                customer_id=customer.id,
                company_id=customer.company_id,
                wash_type=random.choice(wash_type),
                price=round(random.uniform(50, 200), 2),
                notes=None,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )

            db.add(wash)
            washes.append(wash)

    db.commit()


def create_campaigns(customers, db):
    for customer in customers:
        last_wash_days = random.randint(5, 40)

        campaign = Campaign(
            customer_id=customer.id,
            company_id=customer.company_id,
            title="Volte e ganhe desconto",
            message="Sentimos sua falta! Aqui está um cupom para sua próxima lavagem.",
            coupon="WASH10",
            status="active" if last_wash_days > 10 else "sent",
            created_at=datetime.utcnow()
        )


        # campaigns.append(campaign)
        db.add(campaign)

    db.commit()

if __name__ == "__main__":

    customers = create_customers()

    create_washes(customers)
    create_campaigns(customers, db)

    