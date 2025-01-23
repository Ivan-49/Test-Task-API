from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from .keyboards import get_product_keyboard
from .utils import fetch_product_details

class Form(StatesGroup):
    artikul = State()

async def get_product_data(message: types.Message, state: FSMContext):
    await state.set_state(Form.artikul)
    await message.reply("Пожалуйста, введите артикул товара.")

async def process_artikul(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['artikul'] = message.text
    product_details = await fetch_product_details(data['artikul'])
    if product_details:
        await message.reply(f"Данные по товару:\nНазвание: {product_details['name']}\nЦена: {product_details['price']} RUB\nРейтинг: {product_details['rating']}\nКоличество: {product_details['total_quantity']}")
    else:
        await message.reply("Товар не найден.")
    await state.clear()

def register_handlers(dp):
     dp.message.register(get_product_data, F.text.contains("Получить данные по товару"))
     dp.message.register(process_artikul, Form.artikul)