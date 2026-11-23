"""setup для race.py: alice(100) покупает товар(60) — денег хватает на ОДИН."""
from decimal import Decimal
from db import engine, Base, SessionLocal
from models import User, Product, Order
Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
with SessionLocal.begin() as s:
    s.add_all([User(email="alice@example.com", balance=Decimal("100.00")),
               User(email="bob@example.com",   balance=Decimal("1000.00")),
               Product(name="Кофе", price=Decimal("60.00"), stock=100)])
print("setup: alice=100, bob=1000, товар=60, stock=100")
