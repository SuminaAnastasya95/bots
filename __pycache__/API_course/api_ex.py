import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

import requests

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# ⚠️ ИЗМЕНИТЬ ТОКЕН
bot = Bot(token="")
dp = Dispatcher()


# Хэндлер на команду /start ---------------------------------------------------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    botToken = ''  # ТОКЕН БОТА
    channel = 'direcode'  # ЮЗЕРНЕЙМ КАНАЛА
    # API ССЫЛКА
    url = f"https://api.telegram.org/bot{botToken}/getChatMembersCount?chat_id=@{channel}"
    response = requests.get(url)  # ДЕЛАЕМ ГЕТ ЗАПРОС
    data = response.json()  # ПОМЕЩАЕМ ЕГО В JSON
    memberscount = data['result']  # ПРИСВАЕМ ПЕРЕМЕННОЙ ЗНАЧЕНИЕ ИЗ JSON ФАЙЛА

    await message.answer(text=f'В канале {channel} сейчас {memberscount} подписчиков', parse_mode='HTML')


# Запуск процесса поллинга новых апдейтов
async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
