from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} # з'єднання до БД може використовувати тільки той самий потік (thread), в якому воно було створене
)

# False + False - стандарт у веб-додатках (FastAPI, Flask тощо), щоб контролювати, коли зміни зберігаються в базі даних і коли вони надсилаються до неї
SessionLocal = sessionmaker(autocommit=False, # зміни в базі даних не зберігаються автоматично після кожного запиту, треба явно викликати commit() для збереження змін
                            autoflush=False, # SQLAlchemy не буде автоматично надсилати накопичені зміни в базу перед кожним запитом
                            bind=engine)

# базовий клас для моделей SQLAlchemy, який використовує декларативний стиль
# містить усю "магію" для declarative-стилю мапінгу:
# - реєстр мапінгів (registry)
# - метадані (metadata)
# - автоматичне створення таблиць
# - підтримкa type hints (mypy, Pyright, IDE)
class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()