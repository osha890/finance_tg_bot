from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class StartKeyboard:
    enter_token = "Добавить токен"
    my_token = "Мой токен"
    register = "Зарегистрироваться"


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=StartKeyboard.enter_token), KeyboardButton(text=StartKeyboard.my_token)],
        [KeyboardButton(text=StartKeyboard.register)]
    ],
    resize_keyboard=True
)


# ===================================================

class ClearState:
    cancel = "Отмена"


cancel_button_row = [KeyboardButton(text=ClearState.cancel)]

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        cancel_button_row
    ],
    resize_keyboard=True
)
