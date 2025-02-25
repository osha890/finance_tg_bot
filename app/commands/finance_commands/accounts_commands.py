import json

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.config import API_BASE_URL
from finance_tg_bot.app.utils import token_key_if_exists, handle_api_errors
from ...states import CreateAccountState, DeleteAccountState, UpdateAccountState

router = Router()

accounts_url = f"{API_BASE_URL}/accounts/"


# ======== GET ACCOUNTS ===============================================================================

@router.message(Command("accounts"))
@handle_api_errors()
async def list_accounts(message: Message):
    token_key = await token_key_if_exists(message)

    async with aiohttp.ClientSession() as session:
        async with session.get(url=accounts_url,
                               headers={"Authorization": f"Token {token_key}"}) as response:
            response_data = await response.json()
            if response.status == 200:
                accounts = await response.json()
                if accounts:
                    text = "\n".join(
                        [f"ID: {account['id']} - {account['name']}: {account['balance']}" for account in accounts])
                    await message.answer(text)
                else:
                    await message.answer(messages.NO_ACCOUNTS)
            else:
                formatted_error = json.dumps(response_data, indent=4)
                await message.answer(f"{formatted_error}")


# ======== CREATE ACCOUNT ===============================================================================

@router.message(Command("create_account"))
async def create_accounts(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    await state.update_data(token_key=token_key)
    await message.answer(messages.ENTER_ACCOUNT_NAME)
    await state.set_state(CreateAccountState.account_name_create)


@router.message(CreateAccountState.account_name_create)
async def set_account_name(message: Message, state: FSMContext):
    await state.update_data(account_name=message.text.strip())
    await message.answer(messages.ENTER_ACCOUNT_BALANCE)
    await state.set_state(CreateAccountState.account_balance_create)


@router.message(CreateAccountState.account_balance_create)
@handle_api_errors()
async def set_account_balance(message: Message, state: FSMContext):
    state_data = await state.get_data()
    account_name = state_data.get("account_name_create")
    json_data = {
        "name": account_name,
        "balance": message.text.strip(),
    }

    token_key = state_data.get("token_key")

    async with aiohttp.ClientSession() as session:
        async with session.post(url=accounts_url, headers={"Authorization": f"Token {token_key}"},
                                json=json_data) as response:
            response_data = await response.json()
            if response.status == 201:
                await message.answer(messages.ACCOUNT_ADDED)
            elif response_data.get('balance') is not None:
                await message.answer(messages.WRONG_ACCOUNT_BALANCE)
            else:
                formatted_error = json.dumps(response_data, indent=4)
                await message.answer(f"{formatted_error}")

    await state.clear()


# ======== DELETE ACCOUNT ===============================================================================

@router.message(Command("delete_account"))
async def delete_account(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    await state.update_data(token_key=token_key)
    await message.answer(messages.ENTER_ACCOUNT_ID)
    await state.set_state(DeleteAccountState.account_id_delete)


@router.message(DeleteAccountState.account_id_delete)
@handle_api_errors()
async def delete_account(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")
    async with aiohttp.ClientSession() as session:
        async with session.delete(url=f"{accounts_url}{message.text.strip()}/",
                                  headers={"Authorization": f"Token {token_key}"}) as response:
            if response.status == 204:
                await message.answer(messages.ACCOUNT_DELETED)
            else:
                response_data = await response.json()
                formatted_error = json.dumps(response_data, indent=4)
                await message.answer(f"{formatted_error}")

    await state.clear()


# ======== UPDATE ACCOUNT ===============================================================================

@router.message(Command("update_account"))
async def update_account(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
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
        async with aiohttp.ClientSession() as session:
            async with session.patch(url=f"{accounts_url}{account_id}/", headers={"Authorization": f"Token {token_key}"},
                                     json=json_data) as response:
                response_data = await response.json()
                if response.status == 200:
                    await message.answer(messages.ACCOUNT_UPDATED)
                elif response_data.get('balance') is not None:
                    await message.answer(messages.WRONG_ACCOUNT_BALANCE)
                else:
                    formatted_error = json.dumps(response_data, indent=4)
                    await message.answer(f"{formatted_error}")

    await state.clear()
