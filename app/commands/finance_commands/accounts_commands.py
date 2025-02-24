import json

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from finance_tg_bot.config import API_BASE_URL
from ..utils import token_key_if_exists
from ...states import AccountState

router = Router()


@router.message(Command("accounts"))
async def list_accounts(message: Message):
    token_key = await token_key_if_exists(message)

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/accounts/", headers={"Authorization": f"Token {token_key}"}) as response:
            if response.status == 200:
                accounts = await response.json()
                if accounts:
                    text = "\n".join(
                        [f"ID: {account['id']} - {account['name']}: {account['balance']}" for account in accounts])
                    await message.answer(text)
                else:
                    await message.answer("У вас нет счетов.")
            else:
                await message.answer("Ошибка при получении списка счетов.")


@router.message(Command("create_account"))
async def create_accounts(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    await state.update_data(token_key=token_key)
    await message.answer("Введите название счета")
    await state.set_state(AccountState.account_name)


@router.message(AccountState.account_name)
async def register_username(message: Message, state: FSMContext):
    await state.update_data(account_name=message.text.strip())
    await message.answer("Введите баланс")
    await state.set_state(AccountState.account_balance)


@router.message(AccountState.account_balance)
async def register_username(message: Message, state: FSMContext):
    state_data = await state.get_data()
    account_name = state_data.get("account_name")
    json_data = {
        "name": account_name,
        "balance": message.text.strip(),
    }

    token_key = state_data.get("token_key")

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/accounts/", headers={"Authorization": f"Token {token_key}"},
                                json=json_data) as response:
            response_data = await response.json()
            if response.status == 201:
                await message.answer("Аккаунт добавлен")
            elif response_data.get('balance') is not None:
                await message.answer("Неверный формат баланса")
            else:
                formatted_error = json.dumps(response_data, indent=4)
                await message.answer(f"{formatted_error}")

    await state.clear()