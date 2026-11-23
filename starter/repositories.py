"""Дано. Сессия приходит извне; ни commit, ни rollback здесь нет."""
from sqlalchemy import select
from models import User, Product, Order

class UserRepository:
    def __init__(self, session): self.session = session
    def get(self, user_id): return self.session.get(User, user_id)

class ProductRepository:
    def __init__(self, session): self.session = session
    def get(self, product_id): return self.session.get(Product, product_id)

class OrderRepository:
    def __init__(self, session): self.session = session
    def add(self, order): self.session.add(order)
