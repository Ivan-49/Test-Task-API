from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.fsm.context import FSMContext

from fastapi import Depends 

from .keyboards import  info_product_keyboard
from ..utils.database_utils import get_product_info, add_product_to_tasks
from .states import ProductForm, BotState
from ..schemas import Product
from .. models import ScheduledTask
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply("Привет! Я бот для получения данных по товарам.", reply_markup= await info_product_keyboard())
    await state.set_state(BotState.start)    

@router.message(BotState.start, F.text)
async def handle_product_command(message: types.Message, state: FSMContext):
    if message.text == 'Узнать информацию о товаре':
        await message.answer("Введите артикул товара:")
        await state.set_state(BotState.get_product)
    elif message.text == 'Подписаться на товар':
        await message.answer("Введите артикул товара:")
        await state.set_state(BotState.subscribe)

@router.message(BotState.get_product)
async def handle_product_input(message: types.Message, state: FSMContext):
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
            """, reply_markup= await info_product_keyboard())
        else:
            await message.answer('Товар не найден', reply_markup= await info_product_keyboard())
    await state.set_state(BotState.start)


@router.message(BotState.subscribe)
async def handle_product_input(message: types.Message, state: FSMContext):
    try:
        if message.text and message.text.isdigit():
            artikul = message.text
            await add_product_to_tasks(artikul)
            await message.answer("вы успешно подписались на обновление информации о товаре", reply_markup= await info_product_keyboard())
    except Exception as e:
        await message.answer(f"Произошла ошибка, поробуйте позже")
        print(e)
    await state.set_state(BotState.start)
# @router.message()
# async def handle_product_input(message: types.Message):
#     if message.text and message.text.isdigit():
#         artikul = message.text
#         await message.answer("Пожалуйста, подождите...")
#         result = await get_product_info(artikul)
#         if result:
#             await message.answer(f"""
# Название: {result.name}
# Цена: {result.price}       
# Рейтинг: {result.rating}
# Количество: {result.total_quantity}
#             """)
#         else:
#             await message.answer('Товар не найден')