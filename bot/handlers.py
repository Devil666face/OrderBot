import os
from dotenv import load_dotenv
from functools import wraps
from database.models import User
from aiogram import types
from bot.keyboard import (
    Keyboard,
    main_buttons,
)
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from document import (
    for_number,
    last,
    month,
)
from bot.messages import *

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


bot = Bot(
    token=TOKEN,
    parse_mode="HTML",
)
dp = Dispatcher(bot, storage=MemoryStorage())
keyboard = Keyboard()


def bot_poling():
    executor.start_polling(dp, skip_updates=True)


async def answer(message: types.Message, message_text: str) -> None:
    await message.answer(
        message_text,
        reply_markup=keyboard.main,
    )


async def answer_document(tg_id: int, doc_name: str) -> None:
    try:
        await bot.send_document(tg_id, types.InputFile(doc_name, filename=doc_name))
    except Exception as error:
        print(error)


async def answer_admin(message_text: str) -> None:
    await bot.send_message(ADMIN_ID, message_text)


async def task_send_document() -> None:
    doc_name = await last()
    if not doc_name:
        return
    for tg_id in await User.get_all_allow_user_tg_id():
        await answer_document(tg_id, doc_name)
    os.remove(doc_name)


def login(func):
    @wraps(func)
    async def wrapper(message, *args, **kwargs):
        if not await User.is_allow_user(tg_id=message.from_user.id):
            await answer(
                message, "У Вас недостаточно прав, запросите доступ у администратора"
            )
            await answer_admin(
                f"Пользователь {message.from_user.id} {message.from_user.username} не смог получить доступ к действию."
            )
            return
        result = await func(message, *args, **kwargs)
        return result

    return wrapper


class Form(StatesGroup):
    number_line = State()
    number_month = State()


@dp.message_handler(commands=["start"], state=None)
async def start(message: types.Message):
    tg_id = message.from_user.id
    if await User.is_have_user(tg_id, username=message.from_user.username):
        await answer(message, NEW_USER)
        await answer_admin(
            message_text=f"Новый пользователь {message.from_user.id} {message.from_user.username}"
        )
    elif not await User.is_allow_user(tg_id):
        await answer(message, GET_PERMISSIONS)
        await answer_admin(
            message_text=f"Пользователь запрашивает права {message.from_user.id} {message.from_user.username}"
        )

    else:
        await answer(message, ALL_PERMISSIONS)


@dp.message_handler(commands=["allow"], state=None)
async def allow(message: types.Message):
    if message.from_user.id != int(ADMIN_ID):
        return
    tg_id_to_allow = int(message.text.strip().split()[1])
    if await User.set_allow_user(tg_id_to_allow):
        await answer(message, ALLOW_USER)
    else:
        await answer(message, DISSALOW_USER)


@dp.message_handler(Text(equals=main_buttons["for_number"]))
@login
async def make_order_for_number(message: types.Message, state: FSMContext):
    await answer(message, SEND_NUMBER)
    await Form.number_line.set()


@dp.message_handler(state=Form.number_line)
@login
async def get_number(message: types.Message, state: FSMContext):
    if str(message.text).isnumeric():
        doc_name = for_number(int(message.text))
        await answer_document(tg_id=message.from_user.id, doc_name=doc_name)
        os.remove(doc_name)
    else:
        await answer(message, UNCORRECT_NUMBER)
    await state.finish()


@dp.message_handler(Text(equals=main_buttons["for_month"]))
@login
async def make_month_order(message: types.Message, state: FSMContext):
    await answer(message, SEND_MONTH_NUMBER)
    await Form.number_month.set()


@dp.message_handler(state=Form.number_month)
@login
async def get_month(message: types.Message, state: FSMContext):
    if str(message.text).isnumeric():
        doc_name = await month(int(message.text))
        await answer_document(tg_id=message.from_user.id, doc_name=doc_name)
        os.remove(doc_name)
    else:
        await answer(message, UNCORRECT_NUMBER)
    await state.finish()
