from functools import wraps

import aiohttp
from aiogram.types import Message

from finance_tg_bot import messages
from finance_tg_bot.database.crud import get_token
from finance_tg_bot.database.db_settings import get_db


async def token_key_if_exists(message: Message):
    user_id = message.from_user.id
    with get_db() as db:
        token = get_token(db, user_id)
    if not token:
        await message.answer(messages.NO_TOKEN)
        return
    return token.key

def handle_api_errors():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except aiohttp.ClientConnectionError:
                return messages.API_CONNECTION_ERROR
            except Exception as e:
                return f"{str(e)}"
        return wrapper
    return decorator