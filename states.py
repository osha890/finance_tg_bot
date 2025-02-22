from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    username = State()
    password = State()