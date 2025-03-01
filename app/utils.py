import json
import aiohttp

from functools import wraps
from datetime import datetime
from aiogram.types import Message
from aiogram.utils import markdown

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


def make_error_answer(response_data, messages_item):
    if "name" in response_data:
        return messages_item["already_exists"]
    if ("balance" or "type") in response_data:
        return messages_item["wrong_value"]
    formatted_error = json.dumps(response_data, indent=4)
    return f"{formatted_error}"


def get_readable_time(iso_date):
    dt = datetime.fromisoformat(iso_date.rstrip("Z"))  # Убираем 'Z' и преобразуем в datetime
    return dt.strftime("%d.%m.%Y - %H:%M")  # Например, формат "21.02.2025 13:12"


def get_iso_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%d.%m.%Y")  # Пробуем распарсить дату
        return dt.isoformat() + "Z"  # Преобразуем в ISO и добавляем 'Z'
    except ValueError:
        return None  # Если ошибка парсинга, возвращаем None


def get_str_item(item, item_class):
    if item_class == "account":
        return f"ID: {item['id']} - {item['name']}: {item['balance']}"
    elif item_class == "category":
        return f"ID: {item['id']} - {item['name']}: {get_type(item['type'])}"
    elif item_class == "operation":
        return markdown.text(
            f"<b>ID: {item['id']} - {get_type(item['type'])}: {item['amount']}</b>\n",
            f"<i>{item['description']}</i>\n" if item['description'] else "",
            f"{get_readable_time(item['date'])}\n",
            f"Категория ID: {item['category']}\n",
            f"Аккаунт ID: {item['account']}\n",
            "---------------------------------",
            sep=""
        )
    else:
        return "WRONG ITEM"


async def make_answer(response, item_class, messages_item):
    if type(response) == str:
        return response

    rs = response.status

    if rs == 200:
        response_data = await response.json()

        if (response_data and type(response_data) == list) or len(response_data.get("operations")) != 0:
            if item_class == "operation":
                items = response_data.get("operations")
            else:
                items = response_data
            answer_text = "\n".join(
                [get_str_item(item, item_class) for item in items])
            if item_class == "operation":
                answer_text += f"\n\n{messages.TOTAL_AMOUNT}: {response_data.get("total_amount")}"
        elif type(response_data) == dict and "operations" not in response_data:
            item = response_data
            answer_text = markdown.text(
                messages_item["updated"],
                get_str_item(item, item_class),
                sep="\n"
            )
        else:
            answer_text = messages_item["no_items"]

    elif rs == 201:
        response_data = await response.json()
        item = response_data
        answer_text = markdown.text(
            messages_item["added"],
            get_str_item(item, item_class),
            sep="\n"
        )

    elif rs == 204:
        answer_text = messages_item["deleted"]
    elif rs == 403:
        answer_text = messages_item["cant_change"]
    elif rs == 404:
        answer_text = messages_item["not_found"]
    else:
        answer_text = make_error_answer(await response.json(), messages_item)
    return answer_text
