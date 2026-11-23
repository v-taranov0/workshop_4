"""Дано: атомарный create_order уровня вашего ДЗ.
Одна транзакция, откат при сбое — против СБОЯ он корректен.
Против КОНКУРЕНЦИИ — нет. Это вы и исследуете. Правите только этот файл.
"""
from sqlalchemy import select, update
from models import User, Product, Order

class OutOfStockError(Exception): pass
class InsufficientFundsError(Exception): pass

def create_order(session, user_id, product_id):
    with session.begin():
        user = session.get(User, user_id)
        if user is None:
            raise LookupError("Пользователь не найден")
        product = session.get(Product, product_id)
        if product is None:
            raise LookupError("Товар не найден")
        price = product.price
        if product.stock <= 0:
            raise OutOfStockError("Товара нет в наличии")
        if user.balance < price:
            raise InsufficientFundsError("Недостаточно средств")
        user.balance -= price
        product.stock -= 1
        session.add(Order(user_id=user_id, product_id=product_id, amount=price))
