import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from .handlers import get_product_info
from .keyboards import get_product_keyboard
from app.utils import fetch_product_details


BOT_TOKEN = "6422200325:AAE1wLfpb5t0RUWS_pJA-1ORlbnli7boy5Y" #замените на токен своего бота

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для получения данных по товарам.", reply_markup=get_product_keyboard())


@dp.message(F.text.contains("Узнать о товаре"))
async def handle_product_command(message: types.Message):
    await message.answer("Пожалуйста, введите артикул товара:")

@dp.message()
async def handle_product_input(message: types.Message):
    if message.text and message.text.isdigit():
        product_info = await get_product_info(message.text)
        if product_info:
            await message.answer(f"Информация о товаре:\n\n"
                                f"Название: {product_info['name']}\n"
                                f"Цена: {product_info['price']}\n"
                                f"Рейтинг: {product_info['rating']}\n"
                                f"Количество: {product_info['total_quantity']}")
        else:
            await message.answer("Товар с таким артикулом не найден.")
    else:
      await message.answer("Введите корректный артикул товара.")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())