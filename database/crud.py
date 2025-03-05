from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from .models import UserToken


async def get_token(db: AsyncSession, user_id: int):
    result = await db.execute(select(UserToken).filter(UserToken.user_id == user_id))
    return result.scalars().first()


async def save_token(db: AsyncSession, user_id: int, key: str):
    user_token = await get_token(db, user_id)
    if user_token:
        user_token.key = key
    else:
        user_token = UserToken(user_id=user_id, key=key)
        db.add(user_token)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
