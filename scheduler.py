from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tasks import send_latest_news, send_evening_digest
from config import TELEGRAM_BOT_TOKEN
from aiogram import Bot

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_latest_news, "interval", minutes=30, args=[bot])
    scheduler.add_job(send_evening_digest, "cron", hour=21, minute=0, args=[bot])
    scheduler.start()