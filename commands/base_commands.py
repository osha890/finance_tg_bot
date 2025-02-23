from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from finance_tg_bot import messages
from finance_tg_bot.states import UserState

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(messages.START_MESSAGE)


@router.message(Command("setstate"))
async def start_cmd(message: Message):
    UserState.user_id = message.from_user.id
    await message.answer(messages.START_MESSAGE)

