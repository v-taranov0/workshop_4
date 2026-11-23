"""Стенд гонки за балансом (дано, не менять). Гоняет текущий create_order
в двух потоках: alice покупает дважды, денег на один. Запуск: python race.py
Критерий: во всех прогонах успехов=1.
"""
import threading
from decimal import Decimal
from sqlalchemy import select, func
from db import SessionLocal
from models import User, Order
from services import create_order, InsufficientFundsError, OutOfStockError

def buyer(barrier, res):
    barrier.wait()
    try:
        create_order(SessionLocal(), 1, 1)
        res.append("ok")
    except (InsufficientFundsError, OutOfStockError):
        res.append("refused")

def main(trials=10):
    bad = 0
    for i in range(trials):
        with SessionLocal.begin() as s:
            s.query(Order).delete(); s.get(User, 1).balance = Decimal("100.00")
        b = threading.Barrier(2); res = []
        ts = [threading.Thread(target=buyer, args=(b, res)) for _ in range(2)]
        [t.start() for t in ts]; [t.join() for t in ts]
        with SessionLocal() as s:
            bal = s.get(User, 1).balance
            n = s.scalar(select(func.count()).select_from(Order).where(Order.user_id == 1))
        ok = res.count("ok"); bad += ok > 1
        print(f"прогон {i+1}: успехов={ok} balance={bal} заказов={n}" + ("  <-- ПЕРЕРАСХОД" if ok>1 else ""))
    print("ИТОГ:", "ЗЕЛЁНЫЙ (везде 1 успех)" if bad==0 else f"КРАСНЫЙ ({bad} перерасходов)")

if __name__ == "__main__":
    main()
