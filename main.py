
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from dotenv import load_dotenv
import os

from app.handlers.user_handlers import register_user_handlers
from app.utils.logger import setup_logger

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

async def on_startup():
    setup_logger()
    logging.info("Бот запущен.")
    await bot.set_my_commands([
        BotCommand(command="update", description="Принудительно обновить новости")
    ])

def main():
    register_user_handlers(dp)
    asyncio.run(dp.start_polling(bot, on_startup=on_startup))

if __name__ == "__main__":
    main()
