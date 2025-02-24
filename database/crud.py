from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import UserToken


def get_token(db: Session, user_id: int):
    return db.query(UserToken).filter(UserToken.user_id == user_id).first()


def save_token(db: Session, user_id: int, key: str):
    user_token = get_token(db, user_id)
    if user_token:
        user_token.key = key
    else:
        user_token = UserToken(user_id=user_id, key=key)
        db.add(user_token)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
