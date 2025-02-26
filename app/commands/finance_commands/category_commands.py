import json

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from finance_tg_bot import messages
from finance_tg_bot.app.utils import token_key_if_exists, get_type

from ...api_handlers.category_api import list_categories_api
from ...states import GetCategoriesState

router = Router()


# ======== ANSWER MAKERS ===============================================================================

async def make_answer_list_categories(response):
    response_data = await response.json()
    if response.status == 200:
        categories = response_data
        if categories:
            answer_text = "\n".join(
                [f"ID: {category['id']} - {category['name']}: {get_type(category['type'])}" for category in categories])
        else:
            answer_text = messages.NO_CATEGORIES
    else:
        formatted_error = json.dumps(response_data, indent=4)
        answer_text = f"{formatted_error}"
    return answer_text


# ======== GET CATEGORIES ===============================================================================

@router.message(Command("categories"))
async def list_categories(message: Message, state: FSMContext):
    token_key = await token_key_if_exists(message)
    print('hello')
    await state.update_data(token_key=token_key)
    text = markdown.text(
        messages.ENTER_CATEGORY_TYPE,
        '\n',
        messages.SKIP_MESSAGE,
        sep='\n'
    )
    await message.answer(text)
    await state.set_state(GetCategoriesState.category_type)


@router.message(GetCategoriesState.category_type)
async def update_category_type(message: Message, state: FSMContext):
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
