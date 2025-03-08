# Telegram Bot for Finance API

Этот проект представляет собой Telegram-бота, который взаимодействует с API для ведения личной бухгалтерии (Finance API - https://github.com/osha890/finance_api). Бот позволяет управлять финансами, работать с операциями, категорими и счетами, просматривать баланс и анализировать расходы. Бот обладает интутивно понятный интерфейсом, реализованным с помощью клавиатур. Ниже приведен список команд для управления ботом.  

**Начало работы:**  
`/token` - показать токен  
`/token abc123` - добавить токен  
`/register` - зарегистрироваться  

**Операции:**  
`/operations` - показать операции (фильтр)  
`/recent_operations` - показать недавние операции  
`/create_operation` - добавить операцию  
`/delete_operation` - удалить операцию  
`/update_operation` - изменить операцию  

**Счета:**  
`/accounts` - показать счета  
`/create_account` - добавить счет  
`/delete_account` - удалить счет  
`/update_account` - изменить счет  

**Категории:**  
`/categories` - показать категории  
`/create_category` - добавить категорию  
`/delete_category` - удалить категорию  
`/update_category` - изменить категорию  

---

## Стек технологий
- Python 3.12
- aiogram
- SQLAlchemy
- PostgreSQL
- Docker, Dpcker-compose

---

## Создание бота в Telegram

Получите токен для вашего бота через бота `@BotFather` в Telegram.

---

## Установка и запуск с Docker

При этом варианте запуска, помимо контейнеров, необходимых для работы бота, также поднимаются контейнеры для работы Finance API, поэтому бот сможет взаимодействовать с API сразу же после запуска контейнеров.

### 1. Клонирование репозитория
```sh
git clone https://github.com/osha890/finance_tg_bot.git
cd finance_tg_bot
```

### 2. Настройка
Создайте файл `.env.bot` в рабочей директории и укажите необходимые переменные. Пример:
```
POSTGRES_DB=finance_tg_bot
POSTGRES_USER=osha
POSTGRES_PASSWORD=qwerty123

DATABASE_URL=postgresql+asyncpg://osha:qwerty123@localhost/finance_tg_bot  # {dialect}{+driver}://{username}:{password}@{hostname}:{port}/{database}
DATABASE_URL_COMPOSE=postgresql+asyncpg://osha:qwerty123@db_bot/finance_tg_bot

API_BASE_URL = "http://127.0.0.1:8000/api"
API_BASE_URL_COMPOSE = "http://api:8000/api"

BOT_TOKEN="7767300444:AAHmPPIgqI6CO4cr46f38mFL34Fqwldqw4q"  # Токен, который вы получили у @BotFather
```

Создайте файл `.env.api` в рабочей директории и укажите необходимые переменные. Пример:
```
POSTGRES_DB=finance_api
POSTGRES_USER=osha
POSTGRES_PASSWORD=qwerty123
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY='django-insecure-_8su_lkhyoh+2t)%)gpo(5u0t9v!*gf%vtau338*7h($938jp#'
DEBUG=True
```

### 3. Запуск контейнеров
```sh
docker compose up
```

---

## Установка и запуск без Docker

### 1. Клонирование репозитория
```sh
git clone https://github.com/osha890/finance_tg_bot.git
cd finance_tg_bot
```

### 2. Создание виртуального окружения и установка зависимостей
Виртуальное окружение позволяет изолировать зависимости проекта, чтобы избежать конфликтов с глобально установленными пакетами.

#### Создание виртуального окружения
Для macOS и Linux:
```sh
python3 -m venv venv
```
Для Windows:
```sh
python -m venv venv
```

#### Активация виртуального окружения
Для macOS и Linux:
```sh
source venv/bin/activate
```
Для Windows (в командной строке):
```sh
venv\Scripts\activate
```
Для Windows (в PowerShell):
```sh
venv\Scripts\Activate.ps1
```

После активации виртуального окружения в командной строке появится префикс `(venv)`, указывающий, что окружение активно.

#### Установка зависимостей
```sh
pip install -r requirements.txt
```

### 3. Настройка
Создайте базу данных `postgres` с именем `finance_tg_bot`. Затем создайте файл `.env.bot` в рабочей директории и укажите необходимые переменные. Пример:
```
POSTGRES_DB=finance_tg_bot
POSTGRES_USER=osha
POSTGRES_PASSWORD=qwerty123

DATABASE_URL=postgresql+asyncpg://osha:qwerty123@localhost/finance_tg_bot  # {dialect}{+driver}://{username}:{password}@{hostname}:{port}/{database}
DATABASE_URL_COMPOSE=postgresql+asyncpg://osha:qwerty123@db_bot/finance_tg_bot

API_BASE_URL = "http://127.0.0.1:8000/api"
API_BASE_URL_COMPOSE = "http://api:8000/api"

BOT_TOKEN="7767300444:AAHmPPIgqI6CO4cr46f38mFL34Fqwldqw4q"  # Токен, который вы получили у @BotFather
```

В вайле config.py закомментируйте или удалите строчки  
`API_BASE_URL = os.getenv('API_BASE_URL_COMPOSE')`  
`DATABASE_URL = os.getenv('DATABASE_URL_COMPOSE')`  

И раскомментируйте  
`# API_BASE_URL = os.getenv('API_BASE_URL')`  
`# DATABASE_URL = os.getenv('DATABASE_URL')`  

Измененный файл долженть выглядеть так

```
from dotenv import load_dotenv
import os

load_dotenv(".env.bot")

# API_BASE_URL = os.getenv('API_BASE_URL_COMPOSE')
API_BASE_URL = os.getenv('API_BASE_URL')

# DATABASE_URL = os.getenv('DATABASE_URL_COMPOSE')
DATABASE_URL = os.getenv('DATABASE_URL')

BOT_TOKEN = os.getenv('BOT_TOKEN')

```

### 4. Запуск бота
```sh
python main.py
```

### 5. Взаимодействие с API
Для получения возможности взаимодействовать с API запустите на своем компьютере `finance_api` - https://github.com/osha890/finance_api

---

## Проект на github - https://github.com/osha890/finance_tg_bot
