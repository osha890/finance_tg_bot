from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.app.utils import token_key_if_exists, make_answer

from ...api_handlers.category_api import (list_categories_api,
                                          create_category_api,
                                          delete_category_api,
                                          update_category_api)
from ...states import (GetCategoriesState,
                       CreateCategoryState,
                       DeleteCategoryState,
                       UpdateCategoryState)

router = Router()


# ======== GET CATEGORIES ===============================================================================

@router.message(Command("categories"))
async def list_categories(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        text = markdown.text(
            messages.ENTER_CATEGORY_TYPE,
            '\n',
            messages.SKIP_MESSAGE,
            sep='\n'
        )
        await message.answer(text)
        await state.set_state(GetCategoriesState.category_type_get)


@router.message(GetCategoriesState.category_type_get)
async def choose_category_type(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")

    params = {}
    message_text = message.text.strip().lower()
    if message_text == messages.INCOMES.lower():
        params["type"] = "income"
    elif message_text == messages.EXPENSES.lower():
        params["type"] = "expense"
    else:
        pass

    response = await list_categories_api(token_key, params)
    answer_text = await make_answer(response, "category", messages.MESSAGES_CATEGORY)

    await message.answer(answer_text)

    await state.clear()


# ======== CREATE CATEGORY ===============================================================================

@router.message(Command("create_category"))
async def create_category(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)

        await message.answer(messages.ENTER_CATEGORY_NAME)
        await state.set_state(CreateCategoryState.category_name_create)


@router.message(CreateCategoryState.category_name_create)
async def create_category_name(message: Message, state: FSMContext):
    await state.update_data(category_name_create=message.text.strip())

    await message.answer(messages.ENTER_CATEGORY_TYPE)
    await state.set_state(CreateCategoryState.category_type_create)


@router.message(CreateCategoryState.category_type_create)
async def create_category_type(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")
    category_name = state_data.get("category_name_create")

    message_text = message.text.strip().lower()

    types = [messages.INCOMES.lower(), messages.EXPENSES.lower()]
    if message_text in types:
        if message_text == types[0]:
            category_type = "income"
        else:
            category_type = "expense"

        json_data = {
            "name": category_name,
            "type": category_type
        }
        response = await create_category_api(token_key, json_data)
        answer_text = await make_answer(response, "category", messages.MESSAGES_CATEGORY)
        await message.answer(answer_text)
    else:
        await message.answer(messages.CATEGORY_WRONG_TYPE)

    await state.clear()


# ======== DELETE CATEGORY ===============================================================================

@router.message(Command("delete_category"))
async def delete_category(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)

        await message.answer(messages.ENTER_CATEGORY_ID)
        await state.set_state(DeleteCategoryState.category_id_delete)


@router.message(DeleteCategoryState.category_id_delete)
async def delete_category_confirm(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")
    category_id = message.text.strip()

    response = await delete_category_api(token_key, category_id)
    answer_text = await make_answer(response, "category", messages.MESSAGES_CATEGORY)
    await message.answer(answer_text)

    await state.clear()


# ======== UPDATE CATEGORY ===============================================================================

@router.message(Command("update_category"))
async def update_category(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        await message.answer(messages.ENTER_CATEGORY_ID)
        await state.set_state(UpdateCategoryState.category_id_update)


@router.message(UpdateCategoryState.category_id_update)
async def update_category_name(message: Message, state: FSMContext):
    await state.update_data(category_id_update=message.text.strip())
    await message.answer(messages.ENTER_CATEGORY_NAME)
    await state.set_state(UpdateCategoryState.category_name_update)


@router.message(UpdateCategoryState.category_name_update)
async def update_category_type(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")
    category_id = state_data.get("category_id_update")
    category_name = message.text.strip()

    json_data = {"name": category_name}
    response = await update_category_api(token_key, category_id, json_data)
    answer_text = await make_answer(response, "category", messages.MESSAGES_CATEGORY)
    await message.answer(answer_text)

    await state.clear()
