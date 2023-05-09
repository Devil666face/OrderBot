from bot.handlers import (
    bot_poling,
    task_send_document,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.googlesheet import GoogleSheet

if __name__ == "__main__":
    # sheet = GoogleSheet()
    # last_line = sheet.last()
    # last_line.full_clean()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(task_send_document, "interval", minutes=5)
    # scheduler.add_job(task_send_document, "interval", seconds=10)
    scheduler.start()
    bot_poling()
