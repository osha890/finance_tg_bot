import aiohttp
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.config import API_BASE_URL
from finance_tg_bot.states import RegisterState
from finance_tg_bot.db import get_db, save_token, get_token

# user_tokens = {}
router = Router()


@router.message(Command("token"))
async def set_token_cmd(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(messages.TOKEN_HOW_TO)
        return

    token = args[1].strip()
    # user_tokens[message.from_user.id] = token

    # Используем контекстный менеджер для работы с базой данных
    with get_db() as db:  # Контекстный менеджер для работы с сессией
        # Сохраняем токен в базе данных
        save_token(db, message.from_user.id, token)

    await message.answer(messages.TOKEN_SAVED)


@router.message(Command("register"))
async def register_cmd(message: Message, state: FSMContext):
    await message.answer(messages.ENTER_USERNAME)
    await state.set_state(RegisterState.username)


@router.message(RegisterState.username)
async def register_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text.strip())
    await message.answer(messages.ENTER_PASSWORD)
    await state.set_state(RegisterState.password)


@router.message(RegisterState.password)
async def register_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data["username"]
    password = message.text.strip()

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/register/",
                                json={"username": username, "password": password}) as response:
            data = await response.json()
            if response.status == 201:
                token = data.get("token")
                # user_tokens[message.from_user.id] = token

                # Используем контекстный менеджер для работы с базой данных
                with get_db() as db:  # Контекстный менеджер для работы с сессией
                    # Сохраняем токен в базе данных
                    save_token(db, message.from_user.id, token)

                await message.answer(
                    markdown.text(
                        messages.REGISTER_SUCCESS.format(token=token),
                        messages.TOKEN_SAVED,
                        sep='\n'
                    )
                )
            else:
                if data.get("username") is not None:
                    error_message = messages.USER_ALREADY_EXISTS
                else:
                    error_message = str(data)
                await message.answer(messages.REGISTER_ERROR.format(error=error_message))

    await state.clear()
