from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    username = State()
    password = State()

class TokenState(StatesGroup):
    token_key = State()

class AccountState(StatesGroup):
    account_name = State()
    account_balance = State()