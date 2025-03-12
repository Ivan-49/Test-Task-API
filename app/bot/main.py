import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
import os
from dotenv import load_dotenv

from .routers import all_routers

load_dotenv()  # Загружаем переменные окружения

TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher()

for router in all_routers:
    dp.include_router(router)



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
