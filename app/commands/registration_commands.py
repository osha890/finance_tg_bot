import aiohttp

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.enums import ParseMode

from finance_tg_bot import messages
from finance_tg_bot.config import API_BASE_URL
from finance_tg_bot.database.db_settings import get_db
from finance_tg_bot.database.crud import save_token, get_token

from ..states import RegisterState
from finance_tg_bot.app.utils import handle_api_errors
from finance_tg_bot.session import get_session

router = Router()


# ======== API HANDLERS =================================================================

@handle_api_errors()
async def register_api(user_id, json_data):
    session = get_session()
    async with session.post(f"{API_BASE_URL}/register/",
                            json=json_data) as response:
        data = await response.json()
        if response.status == 201:
            token_key = data.get("token")

            with get_db() as db:
                save_token(db, user_id, token_key)

            answer_text = (
                markdown.text(
                    messages.REGISTER_SUCCESS,
                    messages.TOKEN_ANSWER.format(token=token_key),
                    messages.TOKEN_SAVED,
                    sep='\n'
                )
            )
        else:
            if data.get("username") is not None:
                error_message = messages.USER_ALREADY_EXISTS
            else:
                error_message = str(data)
            answer_text = messages.REGISTER_ERROR.format(error=error_message)
        return answer_text


# ======== TOKEN =================================================================

@router.message(Command("token"))
async def token_cmd(message: Message):
    args = message.text.split(maxsplit=1)
    user_id = message.from_user.id
    if len(args) < 2:
        with get_db() as db:
            token = get_token(db, user_id)
        if token:
            text = markdown.text(
                messages.TOKEN_ANSWER.format(token=token.key),
                '\n',
                messages.TOKEN_ADD_HOW_TO,
                sep='\n'
            )
        else:
            text = markdown.text(
                messages.NO_TOKEN,
                '\n',
                messages.TOKEN_ADD_HOW_TO,
                sep='\n'
            )
        await message.answer(text, parse_mode=ParseMode.HTML)
    else:
        key = args[1].strip()

        with get_db() as db:
            save_token(db, user_id, key)

        await message.answer(messages.TOKEN_SAVED)


# ======== REGISTER =================================================================

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
@handle_api_errors()
async def register_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data["username"]
    password = message.text.strip()
    json_data = {"username": username, "password": password}

    # async with aiohttp.ClientSession() as session:
    #     answer_text = await register_api(session, message.from_user.id, json_data)
    #     await message.answer(answer_text, parse_mode=ParseMode.HTML)

    answer_text = await register_api(message.from_user.id, json_data)
    await message.answer(answer_text, parse_mode=ParseMode.HTML)

    await state.clear()
