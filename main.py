import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import messages
from config import TOKEN, API_BASE_URL
from states import RegisterState

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

user_tokens = {}


@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(messages.START_MESSAGE)


@dp.message(Command("token"))
async def set_token(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(messages.TOKEN_HOW_TO)
        return

    token = args[1].strip()
    user_tokens[message.from_user.id] = token
    await message.answer(messages.TOKEN_SAVED)


@dp.message(Command("register"))
async def register_cmd(message: Message, state: FSMContext):
    await message.answer(messages.ENTER_USERNAME)
    await state.set_state(RegisterState.username)


@dp.message(RegisterState.username)
async def register_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text.strip())
    await message.answer(messages.ENTER_PASSWORD)
    await state.set_state(RegisterState.password)


@dp.message(RegisterState.password)
async def register_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data["username"]
    password = message.text.strip()

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/register/",
                                json={"username": username, "password": password}) as response:
            if response.status == 201:
                data = await response.json()
                token = data.get("token")
                user_tokens[message.from_user.id] = token
                await message.answer(messages.REGISTER_SUCCESS.format(token=token))
                await message.answer(messages.TOKEN_SAVED)
            else:
                await message.answer(messages.REGISTER_ERROR)
                await response.text()

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
