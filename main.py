import logging
import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from finance_tg_bot.commands.base_commands import router as base_cmd_router
from finance_tg_bot.commands.registration_commands import router as reg_cmd_router

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_routers(base_cmd_router, reg_cmd_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
