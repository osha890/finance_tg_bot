from dotenv import load_dotenv
import os

load_dotenv(".env.bot")

API_BASE_URL = os.getenv('API_BASE_URL_COMPOSE')
# API_BASE_URL = os.getenv('API_BASE_URL')

DATABASE_URL = os.getenv('DATABASE_URL_COMPOSE')
# DATABASE_URL = os.getenv('DATABASE_URL')

BOT_TOKEN = os.getenv('BOT_TOKEN')
