"""setup для race_stock.py: последний товар (stock=1), у обоих денег вдоволь."""
from decimal import Decimal
from db import engine, Base, SessionLocal
from models import User, Product, Order
Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
with SessionLocal.begin() as s:
    s.add_all([User(email="alice@example.com", balance=Decimal("1000.00")),
               User(email="bob@example.com",   balance=Decimal("1000.00")),
               Product(name="Последний", price=Decimal("60.00"), stock=1)])
print("setup_stock: alice=1000, bob=1000, товар=60, stock=1 (последний)")
