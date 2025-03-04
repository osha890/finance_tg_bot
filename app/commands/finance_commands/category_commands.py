from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from finance_tg_bot import messages
from ...utils import (
    token_key_if_exists,
    make_answer,
    ask_for_id,
    get_id_if_valid)

from ...api_handlers.category_api import (
    list_categories_api,
    create_category_api,
    delete_category_api,
    update_category_api
)

from ...states import (
    GetCategoriesState,
    CreateCategoryState,
    DeleteCategoryState,
    UpdateCategoryState
)
from ...keyboards.common_keyboards import (
    CategoryKBBs,
    TypeKBBs,

    cancel_keyboard,
    category_keyboard,
    types_optional_keyboard,
    types_keyboard,
)

router = Router()


# ======== GET CATEGORIES ===============================================================================

@router.message(F.text == CategoryKBBs.get_categories)
@router.message(Command("categories"))
async def list_categories(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        await message.answer(messages.ENTER_CATEGORY_TYPE, reply_markup=types_optional_keyboard)
        await state.set_state(GetCategoriesState.category_type_get)


@router.message(GetCategoriesState.category_type_get)
async def choose_category_type(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")

    params = {}
    message_text = message.text.strip().lower()
    if message_text == TypeKBBs.income.lower():
        params["type"] = "income"
    elif message_text == TypeKBBs.expense.lower():
        params["type"] = "expense"
    else:
        pass

    response = await list_categories_api(token_key, params)
    answer_text = await make_answer(response, "category", messages.MESSAGES_CATEGORY)

    await message.answer(answer_text, reply_markup=category_keyboard)

    await state.clear()


# ======== CREATE CATEGORY ===============================================================================

@router.message(F.text == CategoryKBBs.create_category)
@router.message(Command("create_category"))
async def create_category(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)

        await message.answer(messages.ENTER_CATEGORY_NAME, reply_markup=cancel_keyboard)
        await state.set_state(CreateCategoryState.category_name_create)


@router.message(CreateCategoryState.category_name_create)
async def create_category_name(message: Message, state: FSMContext):
    await state.update_data(category_name_create=message.text.strip())

    await message.answer(messages.ENTER_CATEGORY_TYPE, reply_markup=types_keyboard)
    await state.set_state(CreateCategoryState.category_type_create)


@router.message(CreateCategoryState.category_type_create)
async def create_category_type(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")
    category_name = state_data.get("category_name_create")

    message_text = message.text.strip().lower()

    types = [TypeKBBs.income.lower(), TypeKBBs.expense.lower()]
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
        await message.answer(answer_text, reply_markup=category_keyboard)
    else:
        await message.answer(messages.CATEGORY_WRONG_TYPE, reply_markup=category_keyboard)

    await state.clear()


# ======== DELETE CATEGORY ===============================================================================


@router.message(F.text == CategoryKBBs.delete_category)
@router.message(Command("delete_category"))
async def delete_category(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        await ask_for_id(message)
        await state.set_state(DeleteCategoryState.category_id_delete)


@router.message(DeleteCategoryState.category_id_delete)
async def delete_category_confirm(message: Message, state: FSMContext):
    state_data = await state.get_data()
    token_key = state_data.get("token_key")

    category_id = await get_id_if_valid(message)
    if not category_id:
        return

    response = await delete_category_api(token_key, category_id)
    answer_text = await make_answer(response, "category", messages.MESSAGES_CATEGORY)
    await message.answer(answer_text, reply_markup=category_keyboard)

    await state.clear()


# ======== UPDATE CATEGORY ===============================================================================

@router.message(F.text == CategoryKBBs.update_category)
@router.message(Command("update_category"))
async def update_category(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    if token_key:
        await state.update_data(token_key=token_key)
        await ask_for_id(message)
        await state.set_state(UpdateCategoryState.category_id_update)


@router.message(UpdateCategoryState.category_id_update)
async def update_category_name(message: Message, state: FSMContext):
    category_id = await get_id_if_valid(message)
    if not category_id:
        return

    await state.update_data(category_id_update=category_id)
    await message.answer(messages.ENTER_CATEGORY_NAME, reply_markup=cancel_keyboard)
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
    await message.answer(answer_text, reply_markup=category_keyboard)

    await state.clear()
