from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from finance_tg_bot import messages

get_back = "К списку действий"
cancel = "Отмена"


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

class ChoseActionKBBs:
    operations = "Операции"
    accounts = "Счета"
    categories = "Категории"


chose_action_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ChoseActionKBBs.operations)],
        [KeyboardButton(text=ChoseActionKBBs.accounts)],
        [KeyboardButton(text=ChoseActionKBBs.categories)],
    ],
    resize_keyboard=True
)


# ===================================================

class AccountKBs:
    get_accounts = "Показать счета"
    create_account = "Добавить счет"
    delete_account = "Удалить счет"
    update_account = "Изменить счет"


account_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=AccountKBs.get_accounts)],
        [KeyboardButton(text=AccountKBs.create_account)],
        [KeyboardButton(text=AccountKBs.delete_account)],
        [KeyboardButton(text=AccountKBs.update_account)],
        [KeyboardButton(text=get_back)],
    ],
    resize_keyboard=True
)
