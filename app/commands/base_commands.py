from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.app.keyboards.common_keyboards import (
    cancel,
    get_back,
    help_request,

    StartKBBs,
    ChoseActionKBBs,

    start_keyboard,
    chose_action_keyboard,
    account_keyboard,
    category_keyboard,
    operation_keyboard,
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

@router.message(F.text == help_request)
@router.message(Command("help"))
async def start_cmd(message: Message):
    await message.answer(
        markdown.text(messages.HELP_MESSAGE),
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


@router.message(F.text == ChoseActionKBBs.categories)
async def work_w_categories(message: Message):
    await  message.answer(
        message.text,
        reply_markup=category_keyboard,
    )

@router.message(F.text == ChoseActionKBBs.operations)
async def work_w_operations(message: Message):
    await  message.answer(
        message.text,
        reply_markup=operation_keyboard,
    )


@router.message(F.text == cancel)
async def clear_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        messages.ACTION_CANCELED,
        reply_markup=chose_action_keyboard
    )
