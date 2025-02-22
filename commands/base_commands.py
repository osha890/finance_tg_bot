from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from finance_tg_bot import messages

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(messages.START_MESSAGE)
