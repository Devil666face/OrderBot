#!/usr/bin/env python
def init_django():
    import django
    from pathlib import Path
    from django.conf import settings

    BASE_DIR = Path(__file__).resolve().parent

    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=[
            "database",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        },
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
