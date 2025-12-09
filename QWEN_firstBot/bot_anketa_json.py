# bot.py
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import os
from dotenv import load_dotenv
# В начало файла, после остальных импортов:
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram import F  # для фильтрации callback-данных
from aiogram.types import CallbackQuery  # тип для обработки нажатий
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import json
from pathlib import Path
SURVEYS_FILE = Path("surveys.json")


class Survey(StatesGroup):
    name = State()
    age = State()
    city = State()
    hobby = State()


# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Токен бота не найден. Проверь .env файл!")

bot = Bot(token=TOKEN)
# ← храним состояния в RAM (для старта — ок)
dp = Dispatcher(storage=MemoryStorage())


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Опрос")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


@dp.message(Command("start"))
async def start_handler(message: Message):
    surveys = load_surveys()
    total = len(surveys)
    if total == 0:
        await message.answer("📭 Пока никто не прошёл опрос.")
        return
    recent = surveys[-5:]
    lines = [f"{i+1}.{s['name']}, {s['age']}, {s['city']}, {s['hobby']}" for i,
             s in enumerate(recent)]
    text = f"📊 Всего анкет: {total}\n\nПоследние 5:\n" + "\n".join(lines)
    await message.answer(text)


@dp.message(Command("survey"), F.text == "📝 Опрос")
async def survey_start(message: Message, state: FSMContext):
    # ← переключаем в состояние "ожидание имени"
    await state.set_state(Survey.name)
    await message.answer("👋 Как тебя зовут?")


@dp.message(Survey.name)
async def survey_name(message: Message, state: FSMContext):
    if not message.text or len(message.text.strip()) < 2:
        await message.answer("Пожалуйста, введи настоящее имя (минимум 2 буквы).")
        return  # остаёмся в том же состоянии
    await state.update_data(name=message.text.strip())
    await state.set_state(Survey.age)
    await message.answer("🔢 Сколько тебе лет?")


@dp.message(Survey.age)
async def survey_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите возраст цифрами, пожалуйста.")
        return
    age = int(message.text)
    if age < 5 or age > 120:
        await message.answer("Возраст должен быть от 5 до 120 лет.")
        return
    await state.update_data(age=age)
    await state.set_state(Survey.city)
    await message.answer("🌇 Из какого ты города?")


@dp.message(Survey.city)
async def survey_city(message: Message, state: FSMContext):
    city = message.text.strip()
    if len(city) < 2:
        await message.answer("Название города должно быть минимум из 2 букв.")
        return
    await state.update_data(city=city)
    await state.set_state(Survey.hobby)
    await message.answer("🧩 Какое твоё хобби?")


@dp.message(Survey.hobby)
async def survey_hobby(message: Message, state: FSMContext):
    hobby = message.text.strip()
    if len(hobby) < 2:
        await message.answer("Опиши подробнее о своем хобби.")
        return
    await state.update_data(hobby=hobby)

    # Получаем все данные
    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    city = data["city"]

    survey_entry = {
        "name": data["name"],
        "age": data["age"],
        "city": data["city"],
        "hobby": data["hobby"],
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Формируем анкету
    text = (
        "✅ Анкета заполнена!\n\n"
        f"👤 Имя: {name}\n"
        f"📅 Возраст: {age}\n"
        f"🏠 Город: {city}\n"
        f"🧩 Хобби: {hobby}\n\n"
        "Спасибо за участие! 🌟"
    )
    restart_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔁 Заполнить снова")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(text, reply_markup=restart_kb)
    surveys = load_surveys()
    surveys.append(survey_entry)
    save_surveys(surveys)

    await state.clear()  # ← ОБЯЗАТЕЛЬНО: выходим из FSM


def load_surveys() -> list:
    if SURVEYS_FILE.exists():
        with open(SURVEYS_FILE, 'r', encoding="utf-8") as f:
            return json.load(f)
    return []


def save_surveys(surveys: list):
    with open(SURVEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(surveys, f, ensure_ascii=False, indent=2)


@dp.message(F.text == '🔁 Заполнить снова')
async def restart_survey(message: Message, state: FSMContext):
    await survey_start(message, state)


async def main():
    print("✅ Бот запущен и ждёт сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
