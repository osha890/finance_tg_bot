import json

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.app.utils import token_key_if_exists, make_error_answer, get_type, get_readable_time, make_answer
from ...api_handlers.operation_api import (
    list_operations_api, create_operation_api, delete_operation_api, update_operation_api, get_recent_operations_api
)

# from ...states import (
#     GetOperationsState, CreateOperationState, DeleteOperationState, UpdateOperationState
# )

router = Router()


# ======== GET OPERATIONS ===============================================================================

@router.message(Command("operations"))
async def list_operations(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        response = await list_operations_api(token_key, {})
        answer_text = await make_answer(response, "operation", messages.MESSAGES_OPERATION)
        await message.answer(answer_text, parse_mode=ParseMode.HTML)

# # ======== CREATE OPERATION ===============================================================================
#
# @router.message(Command("create_operation"))
# async def create_operation(message: Message, state: FSMContext):
#     token_key = await token_key_if_exists(message)
#     if token_key:
#         await state.update_data(token_key=token_key)
#         await message.answer(messages.ENTER_OPERATION_AMOUNT)
#         await state.set_state(CreateOperationState.amount_create)
#
#
# @router.message(CreateOperationState.amount_create)
# async def create_operation_amount(message: Message, state: FSMContext):
#     await state.update_data(amount_create=message.text.strip())
#     await message.answer(messages.ENTER_OPERATION_CATEGORY)
#     await state.set_state(CreateOperationState.category_create)
#
#
# @router.message(CreateOperationState.category_create)
# async def create_operation_category(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     token_key = state_data.get("token_key")
#     amount = state_data.get("amount_create")
#     category = message.text.strip()
#
#     json_data = {"amount": amount, "category": category}
#     response = await create_operation_api(token_key, json_data)
#     answer_text = await make_answer_create_operation(response)
#     await message.answer(answer_text)
#
#     await state.clear()
#
#
# # ======== DELETE OPERATION ===============================================================================
#
# @router.message(Command("delete_operation"))
# async def delete_operation(message: Message, state: FSMContext):
#     token_key = await token_key_if_exists(message)
#     if token_key:
#         await state.update_data(token_key=token_key)
#         await message.answer(messages.ENTER_OPERATION_ID)
#         await state.set_state(DeleteOperationState.operation_id_delete)
#
#
# @router.message(DeleteOperationState.operation_id_delete)
# async def delete_operation_confirm(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     token_key = state_data.get("token_key")
#     operation_id = message.text.strip()
#
#     response = await delete_operation_api(token_key, operation_id)
#     answer_text = await make_answer_delete_operation(response)
#     await message.answer(answer_text)
#
#     await state.clear()
#
#
# # ======== UPDATE OPERATION ===============================================================================
#
# @router.message(Command("update_operation"))
# async def update_operation(message: Message, state: FSMContext):
#     token_key = await token_key_if_exists(message)
#     if token_key:
#         await state.update_data(token_key=token_key)
#         await message.answer(messages.ENTER_OPERATION_ID)
#         await state.set_state(UpdateOperationState.operation_id_update)
#
#
# @router.message(UpdateOperationState.operation_id_update)
# async def update_operation_amount(message: Message, state: FSMContext):
#     await state.update_data(operation_id_update=message.text.strip())
#     await message.answer(messages.ENTER_OPERATION_AMOUNT)
#     await state.set_state(UpdateOperationState.amount_update)
#
#
# @router.message(UpdateOperationState.amount_update)
# async def update_operation_category(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     token_key = state_data.get("token_key")
#     operation_id = state_data.get("operation_id_update")
#     amount = message.text.strip()
#
#     json_data = {"amount": amount}
#     response = await update_operation_api(token_key, operation_id, json_data)
#     answer_text = await make_answer_update_operation(response)
#     await message.answer(answer_text)
#
#     await state.clear()
