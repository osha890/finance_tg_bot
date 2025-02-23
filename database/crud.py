from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from finance_tg_bot.database.models import UserToken


def get_token(db: Session, user_id: int):
    return db.query(UserToken).filter(UserToken.user_id == user_id).first()


def save_token(db: Session, user_id: int, token: str):
    user_token = get_token(db, user_id)
    if user_token:
        user_token.token = token
    else:
        user_token = UserToken(user_id=user_id, token=token)
        db.add(user_token)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
