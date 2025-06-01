from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import send_latest_news, send_evening_digest

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_latest_news, "interval", minutes=30)
    scheduler.add_job(send_evening_digest, "cron", hour=21, minute=0)
    scheduler.start()