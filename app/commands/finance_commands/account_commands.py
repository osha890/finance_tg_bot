from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.app.utils import token_key_if_exists, make_answer

from ...api_handlers.account_api import list_accounts_api, create_account_api, delete_account_api, update_account_api
from ...states import CreateAccountState, DeleteAccountState, UpdateAccountState

router = Router()


# ======== GET ACCOUNTS ===============================================================================

@router.message(Command("accounts"))
async def list_accounts(message: Message):
    token_key = await token_key_if_exists(message)
    if token_key:
        response = await list_accounts_api(token_key)
        answer_text = await make_answer(response, "account", messages.MESSAGES_ACCOUNT)
        await message.answer(answer_text)


# ======== CREATE ACCOUNT ===============================================================================

@router.message(Command("create_account"))
async def create_accounts(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        await message.answer(messages.ENTER_ACCOUNT_NAME)
        await state.set_state(CreateAccountState.account_name_create)


@router.message(CreateAccountState.account_name_create)
async def set_account_name(message: Message, state: FSMContext):
    await state.update_data(account_name_create=message.text.strip())
    await message.answer(messages.ENTER_ACCOUNT_BALANCE)
    await state.set_state(CreateAccountState.account_balance_create)


@router.message(CreateAccountState.account_balance_create)
async def set_account_balance(message: Message, state: FSMContext):
    state_data = await state.get_data()
    account_name = state_data.get("account_name_create")
    json_data = {
        "name": account_name,
        "balance": message.text.strip(),
    }

    token_key = state_data.get("token_key")

    response = await create_account_api(token_key, json_data)
    answer_text = await make_answer(response, "account", messages.MESSAGES_ACCOUNT)
    await message.answer(answer_text)

    await state.clear()


# ======== DELETE ACCOUNT ===============================================================================

@router.message(Command("delete_account"))
async def delete_account(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        await message.answer(messages.ENTER_ACCOUNT_ID)
        await state.set_state(DeleteAccountState.account_id_delete)


@router.message(DeleteAccountState.account_id_delete)
async def delete_account(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")

    response = await delete_account_api(token_key, message.text.strip())
    answer_text = await make_answer(response, "account", messages.MESSAGES_ACCOUNT)
    await message.answer(answer_text)

    await state.clear()


# ======== UPDATE ACCOUNT ===============================================================================

@router.message(Command("update_account"))
async def update_account(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        await message.answer(messages.ENTER_ACCOUNT_ID)
        await state.set_state(UpdateAccountState.account_id_update)


@router.message(UpdateAccountState.account_id_update)
async def update_account_name(message: Message, state: FSMContext):
    message_text = message.text.strip()
    await state.update_data(account_id_update=message_text)
    text = markdown.text(
        messages.ENTER_ACCOUNT_NAME,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(UpdateAccountState.account_name_update)


@router.message(UpdateAccountState.account_name_update)
async def update_account_name(message: Message, state: FSMContext):
    message_text = message.text.strip()
    if message_text.lower() != messages.SKIP.lower():
        await state.update_data(account_name_update=message_text)
    text = markdown.text(
        messages.ENTER_ACCOUNT_BALANCE,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(UpdateAccountState.account_balance_update)


@router.message(UpdateAccountState.account_balance_update)
async def update_account_balance(message: Message, state: FSMContext):
    state_data = await state.get_data()
    account_id = state_data.get("account_id_update")
    account_name = state_data.get("account_name_update")

    message_text = message.text.strip()
    account_balance = message_text if message_text.lower() != messages.SKIP.lower() else None

    json_data = {}
    if account_name is not None:
        json_data["name"] = account_name
    if account_balance is not None:
        json_data["balance"] = account_balance

    if not json_data:
        await message.answer(messages.ACCOUNT_NOT_UPDATED)
    else:
        token_key = state_data.get("token_key")

        response = await update_account_api(token_key, account_id, json_data)
        answer_text = await make_answer(response, "account", messages.MESSAGES_ACCOUNT)
        await message.answer(answer_text)

    await state.clear()
