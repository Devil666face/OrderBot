#!/usr/bin/env python
import os
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DB")


def init_django():
    import django
    from pathlib import Path
    from django.conf import settings

    BASE_DIR = Path(__file__).resolve().parent

    if settings.configured:
        return

    databases = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    if DB != "":
        databases = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": DB,
            }
        }
    settings.configure(
        INSTALLED_APPS=[
            "database",
        ],
        DATABASES=databases,
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
