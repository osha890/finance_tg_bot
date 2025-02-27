import json

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.app.utils import token_key_if_exists, get_type, make_error_answer

from ...api_handlers.category_api import list_categories_api, create_category_api
from ...states import GetCategoriesState, CreateCategoryState

router = Router()


# ======== ANSWER MAKERS ===============================================================================

async def make_answer_list_categories(response):
    if type(response) == str:
        return response
    response_data = await response.json()
    if response.status == 200:
        categories = response_data
        if categories:
            answer_text = "\n".join(
                [f"ID: {category['id']} - {category['name']}: {get_type(category['type'])}" for category in categories])
        else:
            answer_text = messages.NO_CATEGORIES
    else:
        answer_text = make_error_answer(response_data)
    return answer_text


async def make_answer_create_category(response):
    if type(response) == str:
        return response
    if response.status == 201:
        answer_text = messages.CATEGORY_ADDED
    else:
        response_data = await response.json()
        answer_text = make_error_answer(response_data)
    return answer_text


# ======== GET CATEGORIES ===============================================================================

@router.message(Command("categories"))
async def list_categories(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
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
    answer_text = await make_answer_list_categories(response)

    await message.answer(answer_text)

    await state.clear()


# ======== CREATE CATEGORY ===============================================================================

@router.message(Command("create_category"))
async def create_category(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
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
        answer_text = await make_answer_create_category(response)
        await message.answer(answer_text)
    else:
        await message.answer(messages.WRONG_CATEGORY_TYPE)

    await state.clear()
