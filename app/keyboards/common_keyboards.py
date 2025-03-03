from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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

class ClearStateKBBs:
    cancel = "Отмена"


cancel_button_row = [KeyboardButton(text=ClearStateKBBs.cancel)]

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        cancel_button_row
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