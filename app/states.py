from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    username = State()
    password = State()


class TokenState(StatesGroup):
    token_key = State()


class CreateAccountState(StatesGroup):
    account_name_create = State()
    account_balance_create = State()


class DeleteAccountState(StatesGroup):
    account_id_delete = State()


class UpdateAccountState(StatesGroup):
    account_id_update = State()
    account_name_update = State()
    account_balance_update = State()