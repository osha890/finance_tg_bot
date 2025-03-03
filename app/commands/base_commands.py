from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.app.keyboards.common_keyboards import start_keyboard, ClearState

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        markdown.text(
            messages.START_MESSAGE,
            '\n',
            messages.BEGIN_MESSAGE,
            sep='\n'
        ),
        reply_markup=start_keyboard
    )

@router.message(F.text == ClearState.cancel)
async def clear_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        messages.ACTION_CANCELED,
        reply_markup=start_keyboard
    )
