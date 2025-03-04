from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from finance_tg_bot import messages

get_back = "К списку действий"
cancel = "Отмена"
help_request = "Помощь"


# ===================================================

class StartKBBs:
    enter_token = "Добавить токен"
    my_token = "Мой токен"
    register = "Зарегистрироваться"
    get_started = "Начать работу"


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=StartKBBs.enter_token), KeyboardButton(text=StartKBBs.my_token)],
        [KeyboardButton(text=StartKBBs.register)],
        [KeyboardButton(text=StartKBBs.get_started)],
        [KeyboardButton(text=help_request)],
    ],
    resize_keyboard=True
)

# ===================================================


cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=cancel)],
    ],
    resize_keyboard=True
)

skip_and_cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=messages.SKIP)],
        [KeyboardButton(text=cancel)],
    ],
    resize_keyboard=True
)


# ===================================================

class TypeKBBs:
    expense = "Расходы"
    income = "Доходы"
    all_types = "Все"

types_optional_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=TypeKBBs.expense), KeyboardButton(text=TypeKBBs.income)],
        [KeyboardButton(text=TypeKBBs.all_types)],
        [KeyboardButton(text=cancel)],
    ],
    resize_keyboard=True
)

types_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=TypeKBBs.expense), KeyboardButton(text=TypeKBBs.income)],
        [KeyboardButton(text=cancel)],
    ],
    resize_keyboard=True
)

# ===================================================

class ChoseActionKBBs:
    operations = "Операции"
    accounts = "Счета"
    categories = "Категории"


chose_action_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ChoseActionKBBs.operations)],
        [KeyboardButton(text=ChoseActionKBBs.accounts)],
        [KeyboardButton(text=ChoseActionKBBs.categories)],
        [KeyboardButton(text=help_request)],
    ],
    resize_keyboard=True
)


# ===================================================

class AccountKBBs:
    get_accounts = "Показать счета"
    create_account = "Добавить счет"
    delete_account = "Удалить счет"
    update_account = "Изменить счет"


account_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=AccountKBBs.get_accounts)],
        [KeyboardButton(text=AccountKBBs.create_account)],
        [KeyboardButton(text=AccountKBBs.delete_account)],
        [KeyboardButton(text=AccountKBBs.update_account)],
        [KeyboardButton(text=get_back)],
    ],
    resize_keyboard=True
)


# ===================================================

class CategoryKBBs:
    get_categories = "Показать категории"
    create_category = "Добавить категорию"
    delete_category = "Удалить категорию"
    update_category = "Изменить категорию"


category_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=CategoryKBBs.get_categories)],
        [KeyboardButton(text=CategoryKBBs.create_category)],
        [KeyboardButton(text=CategoryKBBs.delete_category)],
        [KeyboardButton(text=CategoryKBBs.update_category)],
        [KeyboardButton(text=get_back)],
    ],
    resize_keyboard=True
)


# ===================================================

class OperationKBBs:
    get_operations = "Показать операции"
    get_recent_operation = "Показать недавние операции"
    create_operation = "Добавить операцию"
    delete_operation = "Удалить операцию"
    update_operation = "Изменить операцию"

operation_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=OperationKBBs.get_operations)],
        [KeyboardButton(text=OperationKBBs.get_recent_operation)],
        [KeyboardButton(text=OperationKBBs.create_operation)],
        [KeyboardButton(text=OperationKBBs.delete_operation)],
        [KeyboardButton(text=OperationKBBs.update_operation)],
        [KeyboardButton(text=get_back)],
    ]
)