from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = "http://127.0.0.1:8000/api"

DATABASE_URL = os.getenv('DATABASE_URL_COMPOSE')
# DATABASE_URL = os.getenv('DATABASE_URL')

BOT_TOKEN = os.getenv('BOT_TOKEN')
