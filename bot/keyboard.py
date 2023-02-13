from aiogram.types import (
    ReplyKeyboardMarkup,
)

main_buttons = {
    "for_number": "Сформировать по номеру",
    "for_month": "Месячный отчет",
}


class Keyboard:
    def __init__(self):
        self.main = self.make_main_buttons()

    def make_main_buttons(self):
        _keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
        for button_label in main_buttons.values():
            _keyboard_main.add(button_label)
        return _keyboard_main
