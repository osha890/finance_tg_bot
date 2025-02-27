from aiogram.fsm.state import State, StatesGroup


# USER STATES

class RegisterState(StatesGroup):
    username = State()
    password = State()


class TokenState(StatesGroup):
    token_key = State()


# ACCOUNT STATES

class CreateAccountState(StatesGroup):
    account_name_create = State()
    account_balance_create = State()


class DeleteAccountState(StatesGroup):
    account_id_delete = State()


class UpdateAccountState(StatesGroup):
    account_id_update = State()
    account_name_update = State()
    account_balance_update = State()


# CATEGORY STATES

class GetCategoriesState(StatesGroup):
    category_type_get = State()


class CreateCategoryState(StatesGroup):
    category_name_create = State()
    category_type_create = State()


class DeleteCategoryState(StatesGroup):
    category_id_delete = State()