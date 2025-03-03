from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.app.keyboards.common_keyboards import (
    cancel,
    get_back,

    StartKBBs,
    ChoseActionKBBs,

    start_keyboard,
    chose_action_keyboard,
    account_keyboard,
)

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


@router.message(F.text == get_back)
@router.message(F.text == StartKBBs.get_started)
async def chose_action(message: Message):
    await message.answer(
        messages.CHOSE_ACTION,
        reply_markup=chose_action_keyboard
    )


@router.message(F.text == ChoseActionKBBs.accounts)
async def work_w_accounts(message: Message):
    await  message.answer(
        message.text,
        reply_markup=account_keyboard,
    )


@router.message(F.text == cancel)
async def clear_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        messages.ACTION_CANCELED,
        reply_markup=start_keyboard
    )
