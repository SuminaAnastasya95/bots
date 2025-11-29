# bot.py
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
import random

# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Токен бота не найден. Проверь .env файл!")

bot = Bot(token=TOKEN)
dp = Dispatcher()
# После инициализации dp (например, после `dp = Dispatcher()`):

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/help"),
            KeyboardButton(text="/info")
        ],
        [
            KeyboardButton(text="❓ Случайный факт")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! 👋 Я простой эхо-бот. Напиши что-нибудь — повторю!",
                         reply_markup=main_keyboard  # ← добавили!
                         )


# @dp.message()
# async def echo_handler(message: Message):
#     if message.text:
#         await message.answer(f"🔁 Ты написал: {message.text.swapcase()}")
#     else:
#         await message.answer("Я пока умею отвечать только на текст. 📝")


@dp.message(Command("help"))
async def help_handler(message: Message):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ℹ️ Подробнее о боте",
                              callback_data="more_info")]
    ])
    await message.answer("Я эхо-бот 🪞\n"
                         "Напиши <code>/start</code>, чтобы начать\n"
                         "Напиши <code>/info</code>, чтобы узнать обо мне",
                         parse_mode="HTML",
                         reply_markup=inline_kb)


@dp.message(Command("info"))
async def info_handler(message: Message):
    await message.answer("🤖 Меня зовут EchoBot.\n"
                         "Я учусь вместе с моим создателем — и скоро стану умнее!\n"
                         "Версия: 0.1")


@dp.callback_query(F.data == 'more_info')
async def more_info_callback(callback: CallbackQuery):
    await callback.message.answer(
        "🔍 Подробности:\n"
        "• Написан на Python + aiogram 3\n"
        "• Использует long polling\n"
        "• Код открыт для обучения 😊"
    )
    await callback.answer()  # обязательно!


FACTS = [
    "🐍 Python назван в честь комедийного шоу 'Летающий цирк Монти Пайтона', а не змеи.",
    "🤖 Telegram API поддерживает до 30 кнопок на одном сообщении.",
    "⚡ Асинхронность (async/await) позволяет боту обрабатывать тысячи пользователей одновременно.",
    "📚 Библиотека aiogram написана на 100% на Python и полностью асинхронна.",
    "💡 Токен бота нельзя никому показывать — иначе им могут завладеть!"
]


@dp.message(F.text == "❓ Случайный факт")
async def fact_handler(message: Message):
    fact = random.choice(FACTS)
    await message.answer(f"🎲 Факт дня:\n\n{fact}")


async def main():
    print("✅ Бот запущен и ждёт сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
