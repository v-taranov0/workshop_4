"""Стенд гонки за складом (дано, не менять). alice и bob одновременно берут
ПОСЛЕДНИЙ товар. Запуск: python race_stock.py  (после setup_stock.py)
Критерий: во всех прогонах успехов=1, stock не отрицательный.
"""
import threading
from decimal import Decimal
from sqlalchemy import select, func
from db import SessionLocal
from models import User, Product, Order
from services import create_order, InsufficientFundsError, OutOfStockError

def buyer(uid, barrier, res):
    barrier.wait()
    try:
        create_order(SessionLocal(), uid, 1)
        res.append("ok")
    except (InsufficientFundsError, OutOfStockError):
        res.append("refused")

def main(trials=10):
    bad = 0
    for i in range(trials):
        with SessionLocal.begin() as s:
            s.query(Order).delete()
            for uid in (1, 2): s.get(User, uid).balance = Decimal("1000.00")
            s.get(Product, 1).stock = 1
        b = threading.Barrier(2); res = []
        ts = [threading.Thread(target=buyer, args=(uid, b, res)) for uid in (1, 2)]
        [t.start() for t in ts]; [t.join() for t in ts]
        with SessionLocal() as s:
            st = s.get(Product, 1).stock
            n = s.scalar(select(func.count()).select_from(Order))
        ok = res.count("ok"); bad += ok > 1
        print(f"прогон {i+1}: успехов={ok} stock={st} заказов={n}" + ("  <-- ДВА взяли последний" if ok>1 else ""))
    print("ИТОГ:", "ЗЕЛЁНЫЙ" if bad==0 else f"КРАСНЫЙ ({bad} двойных продаж)")

if __name__ == "__main__":
    main()
