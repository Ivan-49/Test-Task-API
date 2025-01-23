import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command 
from .handlers import register_handlers
from .keyboards import get_product_keyboard

API_TOKEN = '6422200325:AAE1wLfpb5t0RUWS_pJA-1ORlbnli7boy5Y'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def start_bot():
    register_handlers(dp)
    await dp.start_polling(bot)

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для получения данных по товарам.", reply_markup=get_product_keyboard())

if __name__ == '__main__':
    logging.info("Starting bot...")
    asyncio.run(start_bot())