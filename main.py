import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from finance_tg_bot.config import TOKEN



logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище токенов пользователей (в реальном проекте лучше использовать БД)
user_tokens = {}


# Стартовое меню
def get_main_menu():
    buttons = [[KeyboardButton(text="📊 Мои счета"), KeyboardButton(text="➕ Новый счет")],
               [KeyboardButton(text="💰 Добавить операцию"), KeyboardButton(text="📜 История операций")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привет! Введи свой API токен для авторизации.")


# Обработка токена
@dp.message()
async def handle_token(message: Message):
    token = message.text.strip()
    user_tokens[message.from_user.id] = token
    await message.answer("✅ Авторизация успешна!", reply_markup=get_main_menu())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
