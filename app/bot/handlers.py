from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram import Router

from .keyboards import  info_product_keyboard
from ..utils import get_product_info


router = Router()


@router.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для получения данных по товарам.", reply_markup=info_product_keyboard())

@router.message(F.text.contains("Узнать информацию о товаре"))
async def handle_product_command(message: types.Message):
    await message.answer("Пожалуйста, введите артикул товара:")


@router.message()
async def handle_product_input(message: types.Message):
    if message.text and message.text.isdigit():
        artikul = message.text
        await message.answer("Пожалуйста, подождите...")
        result = await get_product_info(artikul)
        if result:
            await message.answer(f"""
Название: {result.name}
Цена: {result.price}       
Рейтинг: {result.rating}
Количество: {result.total_quantity}
            """)
        else:
            await message.answer('Товар не найден')