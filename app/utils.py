import json
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


def get_type(operation_type):
    if operation_type == 'income':
        result = messages.INCOMES
    elif operation_type == 'expense':
        result = messages.EXPENSES
    else:
        result = messages.UNDEFINED_TYPE
    return result


def get_auth_header(token_key):
    return {"Authorization": f"Token {token_key}"}


def make_error_answer(response_data):
    formatted_error = json.dumps(response_data, indent=4)
    return f"{formatted_error}"
