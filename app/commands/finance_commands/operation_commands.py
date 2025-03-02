import json

from pprint import pprint
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.app.utils import token_key_if_exists, make_error_answer, get_type, get_readable_time, make_answer, \
    get_iso_date
from ...api_handlers.operation_api import (
    list_operations_api, create_operation_api, delete_operation_api, update_operation_api, get_recent_operations_api
)

from ...states import (
    GetOperationsState, CreateOperationState, DeleteOperationState, UpdateOperationState, RecentOperationsState
)

router = Router()


# ======== GET OPERATIONS ===============================================================================

@router.message(Command("operations"))
async def list_operations(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        text = markdown.text(
            messages.ENTER_OPERATION_TYPE,
            '\n',
            messages.SKIP_MESSAGE,
            sep='\n'
        )
        await message.answer(text)
        await state.set_state(GetOperationsState.operation_type_get)


async def ask_for_date(message: Message):
    text = markdown.text(
        messages.ENTER_OPERATION_DATE,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)


@router.message(GetOperationsState.operation_type_get)
async def create_operation_type(message: Message, state: FSMContext):
    message_text = message.text.strip().lower()
    if message_text == messages.INCOMES.lower():
        await state.update_data(operation_type_get="income")
    elif message_text == messages.EXPENSES.lower():
        await state.update_data(operation_type_get="expense")
    else:
        pass
    await ask_for_date(message, state)
    await state.set_state(GetOperationsState.operation_date_get)


@router.message(GetOperationsState.operation_date_get)
async def create_operation_date(message: Message, state: FSMContext):
    message_text = message.text.strip()
    if message_text.lower() == messages.SKIP.lower():
        text = markdown.text(
            messages.ENTER_OPERATION_DATE_AFTER,
            '\n',
            messages.SKIP_MESSAGE,
            sep='\n'
        )
        await message.answer(text)
        await state.set_state(GetOperationsState.operation_date_after_get)
    else:
        iso_date = get_iso_date(message_text)
        if iso_date is not None:
            await state.update_data(operation_date_get=iso_date)
            text = markdown.text(
                messages.ENTER_OPERATION_ACCOUNT,
                '\n',
                messages.SKIP_MESSAGE,
                sep='\n'
            )
            await message.answer(text)
            await state.set_state(GetOperationsState.operation_account_get)
        else:
            await message.answer(messages.OPERATION_WRONG_DATE)
            await ask_for_date(message, state)


@router.message(GetOperationsState.operation_date_after_get)
async def create_operation_date_after(message: Message, state: FSMContext):
    iso_date = get_iso_date(message.text.strip())
    if iso_date is not None:
        await state.update_data(operation_date_after_get=iso_date)
    text = markdown.text(
        messages.ENTER_OPERATION_DATE_BEFORE,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(GetOperationsState.operation_date_before_get)


@router.message(GetOperationsState.operation_date_before_get)
async def create_operation_date_before(message: Message, state: FSMContext):
    iso_date = get_iso_date(message.text.strip())
    if iso_date is not None:
        await state.update_data(operation_date_before_get=iso_date)
    text = markdown.text(
        messages.ENTER_OPERATION_ACCOUNT,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(GetOperationsState.operation_account_get)


@router.message(GetOperationsState.operation_account_get)
async def create_operation_account(message: Message, state: FSMContext):
    message_text = message.text.strip()
    if message_text.lower() != messages.SKIP.lower():
        await state.update_data(operation_account_get=message_text)
    text = markdown.text(
        messages.ENTER_OPERATION_CATEGORY,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(GetOperationsState.operation_category_get)


@router.message(GetOperationsState.operation_category_get)
async def create_operation_account(message: Message, state: FSMContext):
    state_data = await state.get_data()
    message_text = message.text.strip()
    token_key = state_data.get("token_key")
    params = {}
    if state_data.get("operation_type_get") is not None:
        params["type"] = state_data.get("operation_type_get")
    if state_data.get("operation_date_get") is not None:
        params["date"] = state_data.get("operation_date_get")
    if state_data.get("operation_date_after_get") is not None:
        params["date_after"] = state_data.get("operation_date_after_get")
    if state_data.get("operation_date_before_get") is not None:
        params["date_before"] = state_data.get("operation_date_before_get")
    if state_data.get("operation_account_get") is not None:
        params["account"] = state_data.get("operation_account_get")
    if message_text.lower() != messages.SKIP.lower():
        params["category"] = message_text
    pprint(params)
    response = await list_operations_api(token_key, params)
    answer_text = await make_answer(response, "operation", messages.MESSAGES_OPERATION)

    await message.answer(answer_text, parse_mode=ParseMode.HTML)

    await state.clear()


# ======== CREATE OPERATION ===============================================================================

@router.message(Command("create_operation"))
async def create_operation(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)

        await message.answer(messages.ENTER_OPERATION_TYPE)
        await state.set_state(CreateOperationState.operation_type_create)


@router.message(CreateOperationState.operation_type_create)
async def create_operation_type(message: Message, state: FSMContext):
    message_text = message.text.strip().lower()
    types = [messages.INCOMES.lower(), messages.EXPENSES.lower()]
    if message_text in types:
        operation_type = "income" if message_text == types[0] else "expense"
        await state.update_data(operation_type_create=operation_type)

        await message.answer(messages.ENTER_OPERATION_AMOUNT)
        await state.set_state(CreateOperationState.operation_amount_create)
    else:
        await message.answer(messages.OPERATION_WRONG_TYPE)


@router.message(CreateOperationState.operation_amount_create)
async def create_operation_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError
        await state.update_data(operation_amount_create=amount)

        await message.answer(messages.ENTER_OPERATION_ACCOUNT)
        await state.set_state(CreateOperationState.operation_account_create)
    except ValueError:
        await message.answer(messages.OPERATION_WRONG_AMOUNT)


@router.message(CreateOperationState.operation_account_create)
async def create_operation_account(message: Message, state: FSMContext):
    await state.update_data(operation_account_create=message.text.strip())

    await message.answer(messages.ENTER_OPERATION_CATEGORY)
    await state.set_state(CreateOperationState.operation_category_create)


@router.message(CreateOperationState.operation_category_create)
async def create_operation_category(message: Message, state: FSMContext):
    await state.update_data(operation_category_create=message.text.strip())

    text = markdown.text(
        messages.ENTER_OPERATION_DESCRIPTION,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(CreateOperationState.operation_description_create)


@router.message(CreateOperationState.operation_description_create)
async def create_operation_description(message: Message, state: FSMContext):
    message_text = message.text.strip()
    state_data = await state.get_data()
    token_key = state_data.get("token_key")
    operation_type = state_data.get("operation_type_create")
    amount = state_data.get("operation_amount_create")
    account = state_data.get("operation_account_create")
    category = state_data.get("operation_category_create")
    description = message_text if message_text.lower() != messages.SKIP.lower() else None

    json_data = {
        "type": operation_type,
        "amount": amount,
        "account": account,
        "category": category,
        "description": description
    }

    pprint(json_data)
    response = await create_operation_api(token_key, json_data)
    answer_text = await make_answer(response, "operation", messages.MESSAGES_OPERATION)
    await message.answer(answer_text, parse_mode=ParseMode.HTML)

    await state.clear()


# ======== DELETE OPERATION ===============================================================================

@router.message(Command("delete_operation"))
async def delete_operation(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        await message.answer(messages.ENTER_OPERATION_ID)
        await state.set_state(DeleteOperationState.operation_id_delete)


@router.message(DeleteOperationState.operation_id_delete)
async def delete_operation_confirm(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")
    operation_id = message.text.strip()

    response = await delete_operation_api(token_key, operation_id)
    answer_text = await make_answer(response, "operation", messages.MESSAGES_OPERATION)
    await message.answer(answer_text)

    await state.clear()


# ======== UPDATE OPERATION ===============================================================================

@router.message(Command("update_operation"))
async def update_operation(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        await message.answer(messages.ENTER_OPERATION_ID)
        await state.set_state(UpdateOperationState.operation_id_update)


@router.message(UpdateOperationState.operation_id_update)
async def update_operation_id(message: Message, state: FSMContext):
    await state.update_data(operation_id_update=message.text.strip())

    text = markdown.text(
        messages.ENTER_OPERATION_AMOUNT,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(UpdateOperationState.operation_amount_update)


@router.message(UpdateOperationState.operation_amount_update)
async def update_operation_amount(message: Message, state: FSMContext):
    message_text = message.text.strip()
    if message_text.lower() != messages.SKIP.lower():
        try:
            amount = float(message_text)
            await state.update_data(operation_amount_update=amount)
        except ValueError:
            await message.answer(messages.OPERATION_WRONG_AMOUNT)
            return

    text = markdown.text(
        messages.ENTER_OPERATION_ACCOUNT,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(UpdateOperationState.operation_account_update)


@router.message(UpdateOperationState.operation_account_update)
async def update_operation_account(message: Message, state: FSMContext):
    message_text = message.text.strip()
    if message_text.lower() != messages.SKIP.lower():
        await state.update_data(operation_account_update=message_text)

    text = markdown.text(
        messages.ENTER_OPERATION_CATEGORY,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(UpdateOperationState.operation_category_update)


@router.message(UpdateOperationState.operation_category_update)
async def update_operation_category(message: Message, state: FSMContext):
    message_text = message.text.strip()
    if message_text.lower() != messages.SKIP.lower():
        await state.update_data(operation_category_update=message_text)

    text = markdown.text(
        messages.ENTER_OPERATION_DESCRIPTION,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(UpdateOperationState.operation_description_update)


@router.message(UpdateOperationState.operation_description_update)
async def update_operation_description(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")
    operation_id = state_data.get("operation_id_update")
    amount = state_data.get("operation_amount_update")
    account = state_data.get("operation_account_update")
    category = state_data.get("operation_category_update")
    message_text = message.text.strip()
    if message_text.lower() != messages.SKIP.lower():
        description = message_text
    else:
        description = None

    json_data = {}
    if amount:
        json_data["amount"] = amount
    if account:
        json_data["account"] = account
    if category:
        json_data["category"] = category
    if description is not None:
        json_data["description"] = description

    pprint(json_data)

    if json_data:
        response = await update_operation_api(token_key, operation_id, json_data)
        answer_text = await make_answer(response, "operation", messages.MESSAGES_OPERATION)
        await message.answer(answer_text)
    else:
        await message.answer(messages.OPERATION_NOT_UPDATED)

    await state.clear()


# ======== RECENT OPERATIONS ===============================================================================

@router.message(Command("recent_operations"))
async def recent_operations(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        text = markdown.text(
            messages.ENTER_OPERATION_TYPE,
            '\n',
            messages.SKIP_MESSAGE,
            sep='\n'
        )
        await message.answer(text)
        await state.set_state(RecentOperationsState.operation_type_recent)


@router.message(RecentOperationsState.operation_type_recent)
async def recent_operations_type(message: Message, state: FSMContext):
    message_text = message.text.strip()
    if message_text.lower() != messages.SKIP.lower():
        types = [messages.INCOMES.lower(), messages.EXPENSES.lower()]
        if message_text in types:
            operation_type = "income" if message_text == types[0] else "expense"
            await state.update_data(operation_type_recent=operation_type)

    await message.answer(messages.ENTER_OPERATIONS_COUNT)
    await state.set_state(RecentOperationsState.operations_count_recent)


@router.message(RecentOperationsState.operations_count_recent)
async def recent_operations_count(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")
    operation_type = state_data.get("operation_type_recent")

    try:
        operations_count = int(message.text.strip())
    except ValueError:
        await message.answer(messages.WRONG_VALUE)
        return

    json_data = {
        "count": operations_count
    }

    if operation_type:
        json_data["type"] = operation_type.lower()


    response = await get_recent_operations_api(token_key, json_data)
    answer_text = await make_answer(response, "operation", messages.MESSAGES_OPERATION)
    await message.answer(answer_text, parse_mode=ParseMode.HTML)

    await state.clear()
