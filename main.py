from bot.handlers import (
    bot_poling,
    task_send_document,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(task_send_document, "interval", minutes=5)
    # scheduler.add_job(task_send_document, "interval", seconds=10)
    scheduler.start()
    bot_poling()
