from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from finance_tg_bot import messages

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await message.answer(
        markdown.text(
            messages.START_MESSAGE,
            '\n',
            messages.BEGIN_MESSAGE,
            sep='\n'
        )
    )
