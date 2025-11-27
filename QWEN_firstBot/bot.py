# bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Токен бота не найден. Проверь .env файл!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! 👋 Я простой эхо-бот. Напиши что-нибудь — повторю!")


# @dp.message()
# async def echo_handler(message: Message):
#     if message.text:
#         await message.answer(f"🔁 Ты написал: {message.text.swapcase()}")
#     else:
#         await message.answer("Я пока умею отвечать только на текст. 📝")


@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Я эхо-бот 🪞\n"
                         "Напиши <code>/start</code>, чтобы начать\n"
                         "Напиши <code>/info</code>, чтобы узнать обо мне",
                         parse_mode="HTML")


@dp.message(Command("info"))
async def info_handler(message: Message):
    await message.answer("🤖 Меня зовут EchoBot.\n"
                         "Я учусь вместе с моим создателем — и скоро стану умнее!\n"
                         "Версия: 0.1")


async def main():
    print("✅ Бот запущен и ждёт сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
