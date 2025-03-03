START_MESSAGE = "Привет! Я бот для ведения личной бухгалтерии."
BEGIN_MESSAGE = "Для начала работы добавьте свой токен или зарегистрируйтесь."

HELP_MESSAGE = """help message"""

TOKEN_ADD_HOW_TO = """Чтобы добавить или изменить токен, используйте команду /token с аргументом.
Например: /token 2uj3tg14fwq124we3fcf23"""
TOKEN_SAVED = "Токен успешно сохранен"
TOKEN_ANSWER = "Ваш токен: <code>{token}</code>"
NO_TOKEN = "Токен не найден"
ENTER_TOKEN = "Введите токен"

EXPENSES = "Расходы"
INCOMES = "Доходы"
UNDEFINED_TYPE = "Неизвестный тип"

ENTER_USERNAME = "Введите username"
ENTER_PASSWORD = "Введите password"
REGISTER_SUCCESS = "Регистрация завершена!"
REGISTER_ERROR = "Ошибка регистрации: {error}"
USER_ALREADY_EXISTS = "Пользователь с таким именем уже существует"
KEEP_YOUR_TOKEN = "<u><i>Сохраните ваш токен. Он может понадобиться для аутентификации</i></u>"

NO_ACCOUNTS = "Нет счетов"
ENTER_ACCOUNT_NAME = "Введите название счета"
ENTER_ACCOUNT_BALANCE = "Введите баланс счета"
ENTER_ACCOUNT_ID = "Введите ID счёта"
ACCOUNT_ADDED = "Счет успешно добавлен"
ACCOUNT_DELETED = "Счет успешно удален"
ACCOUNT_UPDATED = "Счет успешно изменен"
ACCOUNT_NOT_UPDATED = "Счет не был изменен"
ACCOUNT_WRONG_BALANCE = "Неверный формат баланса"
ACCOUNT_ALREADY_EXISTS = "Счет с таким именем уже существует"
ACCOUNT_NOT_FOUND = "Счет не найден"

NO_CATEGORIES = "Нет категорий"
ENTER_CATEGORY_NAME = "Введите название категории"
ENTER_CATEGORY_ID = "Введите ID категории"
ENTER_CATEGORY_TYPE = f"Введите тип категории ({EXPENSES}/{INCOMES})"
CATEGORY_ADDED = "Категория успешно добавлена"
CATEGORY_DELETED = "Категория успешно удалена. Если к ней были прикреплены операции, они перенесены на дефолтные категории"
CATEGORY_UPDATED = "Категория успешно изменена"
CATEGORY_NOT_UPDATED = "Категория не была изменена"
CATEGORY_CANT_CHANGE = "Вы не можете изменить или удалить эту категорию"
CATEGORY_WRONG_TYPE = "Неверный тип категории"
CATEGORY_ALREADY_EXISTS = "Категория с таким именем уже существует"
CATEGORY_NOT_FOUND = "Категория не найдена"

NO_OPERATIONS = "Нет операций"
ENTER_OPERATION_AMOUNT = "Введите сумму операции"
ENTER_OPERATION_ID = "Введите ID операции"
ENTER_OPERATION_TYPE = f"Введите тип операции ({EXPENSES}/{INCOMES})"
ENTER_OPERATION_DATE = "Введите дату операции в формате ДД.ММ.ГГГГ"
ENTER_OPERATION_DATE_AFTER = "Введите нижний порог даты в формате ДД.ММ.ГГГГ"
ENTER_OPERATION_DATE_BEFORE = "Введите верхний порог даты в формате ДД.ММ.ГГГГ"
ENTER_OPERATION_ACCOUNT = "Введите счет операции"
ENTER_OPERATION_CATEGORY = "Введите категорию операции"
ENTER_OPERATION_DESCRIPTION = "Введите описание операции"
ENTER_OPERATIONS_COUNT = "Введите количество операций"
OPERATION_WRONG_DATE = "Неверный формат даты"
OPERATION_ADDED = "Операция успешно добавлена"
OPERATION_DELETED = "Операция успешно удалена"
OPERATION_UPDATED = "Операция успешно изменена"
OPERATION_NOT_UPDATED = "Операция не была изменена"
OPERATION_WRONG_AMOUNT = "Неверный формат суммы"
OPERATION_WRONG_TYPE = "Неверный тип операции"
OPERATION_ALREADY_EXISTS = "Операция с таким названием уже существует"
OPERATION_NOT_FOUND = "Операция не найдена"
TOTAL_AMOUNT = "Результат по операциям"

MESSAGES_ACCOUNT = {
    "no_items": "Нет счетов",
    "added": "Счет успешно добавлен",
    "deleted": "Счет успешно удален",
    "updated": "Счет успешно изменен",
    "wrong_value": "Неверный формат баланса",
    "already_exists": "Счет с таким именем уже существует",
    "not_found": "Счет не найден"
}

MESSAGES_CATEGORY = {
    "no_items": "Нет категорий",
    "added": "Категория успешно добавлена",
    "deleted": "Категория успешно удалена. Если к ней были прикреплены операции, они перенесены на дефолтные категории",
    "updated": "Категория успешно изменена",
    "cant_change": "Вы не можете изменить или удалить эту категорию",
    "wrong_value": "Неверный тип категории",
    "already_exists": "Категория с таким именем уже существует",
    "not_found": "Категория не найдена"
}

MESSAGES_OPERATION = {
    "no_items": "Нет операций",
    "added": "Операция успешно добавлена",
    "deleted": "Операция успешно удалена",
    "updated": "Операция успешно изменена",
    "wrong_value": "Неверный формат суммы",
    "already_exists": "Операция с таким названием уже существует",
    "not_found": "Операция не найдена"
}

API_CONNECTION_ERROR = "Отсутствует соединение с API. Попробуйте позже"
SKIP = "Далее"
SKIP_MESSAGE = f"Если хотите пропустить этот шаг, отправьте '{SKIP}'"


WRONG_VALUE = "Неверный формат"

ACTION_CANCELED = "Действие отменено"
CHOSE_ACTION = "Выберите действие"