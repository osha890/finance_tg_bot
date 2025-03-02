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


class UpdateCategoryState(StatesGroup):
    category_id_update = State()
    category_name_update = State()
    category_type_update = State()


# OPERATION STATES

class GetOperationsState(StatesGroup):
    operation_type_get = State()
    operation_date_get = State()
    operation_date_after_get = State()
    operation_date_before_get = State()
    operation_account_get = State()
    operation_category_get = State()


class CreateOperationState(StatesGroup):
    operation_type_create = State()
    operation_amount_create = State()
    operation_account_create = State()
    operation_category_create = State()
    operation_description_create = State()


class DeleteOperationState(StatesGroup):
    operation_id_delete = State()


class UpdateOperationState(StatesGroup):
    operation_id_update = State()
    operation_amount_update = State()
    operation_account_update = State()
    operation_category_update = State()
    operation_description_update = State()


class RecentOperationsState(StatesGroup):
    operation_type_recent = State()
    operations_count_recent = State()
