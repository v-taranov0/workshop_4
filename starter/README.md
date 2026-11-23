## Настройка
```bash
pip install "sqlalchemy>=2.0" psycopg2-binary alembic
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/workshop"
```
### Создание БД с помощью docker
```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

## Файлы
- `db.py`, `models.py`, `repositories.py` — даны, не меняете.
- `services.py` — базовый атомарный `create_order`. **Только его вы и правите.**
- `race.py` — стенд гонки за балансом (тест). НЕ меняете.
- `race_stock.py` — стенд гонки за складом (вызов 4). НЕ меняете.
- `setup.py` / `setup_stock.py` — данные для стендов.

## Как мерить
```bash
python setup.py && python race.py            # вызовы 1–3: цель — ЗЕЛЁНЫЙ
python setup_stock.py && python race_stock.py # вызов 4: цель — ЗЕЛЁНЫЙ
```
«Зелёный» — это 10 прогонов подряд с одним успехом.