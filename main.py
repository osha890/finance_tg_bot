import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from app.commands.base_commands import router as base_cmd_router
from app.commands.registration_commands import router as reg_cmd_router
from app.commands.finance_commands.account_commands import router as acc_cmd_router
from app.commands.finance_commands.category_commands import router as cat_cmd_router
from app.commands.finance_commands.operation_commands import router as opr_cmd_router
from database.db_settings import init_db
from session import get_session, close_session

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
bot.default = DefaultBotProperties(parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_routers(base_cmd_router,
                   reg_cmd_router,
                   acc_cmd_router,
                   cat_cmd_router,
                   opr_cmd_router)


async def main():
    await init_db()
    session = get_session()
    try:
        await dp.start_polling(bot)
    finally:
        await close_session()


if __name__ == "__main__":
    asyncio.run(main())
