from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from finance_tg_bot.config import DATABASE_URL

Base = declarative_base()


# Модель для хранения токенов пользователей
class UserToken(Base):
    __tablename__ = 'user_tokens'

    user_id = Column(BigInteger, primary_key=True, index=True)
    token = Column(String)


# Создаем синхронный движок и сессию
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для создания таблиц в базе данных
def init_db():
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Функция для получения токена пользователя по user_id
def get_token(db: Session, user_id: int):
    return db.query(UserToken).filter(UserToken.user_id == user_id).first()


# Функция для сохранения токена в базе данных
def save_token(db: Session, user_id: int, token: str):
    # Проверяем, существует ли уже токен для этого пользователя
    user_token = get_token(db, user_id)
    if user_token:
        # Если токен есть, обновляем его
        user_token.token = token
    else:
        # Если токена нет, создаем новый
        user_token = UserToken(user_id=user_id, token=token)
        db.add(user_token)

    try:
        db.commit()  # Сохраняем изменения в базе данных
    except IntegrityError:
        db.rollback()  # Откатываем изменения в случае ошибки
