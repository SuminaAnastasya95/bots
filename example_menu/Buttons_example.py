import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import example_menu.config as config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    button1 = types.InlineKeyboardButton(
        text=config.btn1_name, callback_data="btn1")  # СОЗДАНИЕ КНОПКИ №1 callback_data="btn1" это описание, что будет приходить в ответ. Мы нажимаем кнопку нам приходит ответ с названием из функции btn1
    button2 = types.InlineKeyboardButton(
        text=config.btn2_name, callback_data="btn2")  # СОЗДАНИЕ КНОПКИ №2
    button3 = types.InlineKeyboardButton(
        text=config.btn3_name, callback_data="btn3")  # СОЗДАНИЕ КНОПКИ №3
    button4 = types.InlineKeyboardButton(
        text=config.btn4_name, url="https://github.com/SuminaAnastasya95/dz-demo")  # СОЗДАНИЕ КНОПКИ №4
    # СОЗДАНИЕ СТРОКИ 1 С КНОПКАМИ т.е. расположение кнопок
    builder.row(button1, button2)
    builder.row(button3, button4)  # СОЗДАНИЕ СТРОКИ 2 С КНОПКАМИ
    await bot.send_photo(message.chat.id, photo=config.photo_url, caption=config.menu_text, reply_markup=builder.as_markup())
    # message.chat.id - это наш чат с ботом, photo - вызываем отображение фото, caption подпись под фото, reply_markup - вызов отображения меню


@dp.callback_query(F.data == "btn1")
async def cmd_price(callback: types.CallbackQuery):
    await callback.answer()
    # ОТПРАВКА ОТВЕТА НА КНОПКУ №1
    # type: ignore
    await callback.message.answer(config.btn1_response, parse_mode='HTML')


@dp.callback_query(F.data == "btn2")
async def cmd_price(callback: types.CallbackQuery):
    await callback.answer()
    # ОТПРАВКА ОТВЕТА НА КНОПКУ №2
    # type: ignore
    await callback.message.answer(config.btn2_response, parse_mode='HTML')


@dp.callback_query(F.data == "btn3")
async def cmd_price(callback: types.CallbackQuery):
    await callback.answer()
    # ОТПРАВКА ОТВЕТА НА КНОПКУ №3
    # type: ignore
    await callback.message.answer(config.btn3_response, parse_mode='HTML')


@dp.callback_query(F.data == "btn4")
async def cmd_price(callback: types.CallbackQuery):
    await callback.answer()
    # ОТПРАВКА ОТВЕТА НА КНОПКУ №4
    # type: ignore
    await callback.message.answer(config.btn4_response, parse_mode='HTML')


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
