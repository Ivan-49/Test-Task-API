from aiogram import types, F
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os

from ..keyboards import start_keyboard, item_keyboard, sub_keyboard
from ..states import BotState
from ...utils.data_base_communications.get_item import get_item

router = Router()


@router.message(
    BotState.get_product_article, F.text == "Получить данные за последнее время"
)
async def get_product(message: types.Message, state: FSMContext):
    article = await state.get_data()
    article = article.get("artikul")
    item = await get_item(article, 28)
    if item:
        response = ""
        for i in item:
            date = i[5]
            price = i[3]
            count = i[4]
            rating = i[6]
            response += f"Дата: {date}\nЦена: {price}\nКоличество: {count}\nРейтинг: {rating}\n\n"

        name = i[1]
        artikul = i[0]

        await message.answer(f"Название: {name}\nАртикул: {artikul}\n\n{response}")
        await message.answer(
            "Теперь вы можете сделать что то с следющим товаром, просто скинте мне новый артикул"
        )
        await state.set_state(BotState.wainting_article)
    else:
        await message.answer(
            "Товар не найден в нашей базе, но вы можете сделать так что бы информация об этом товаре появилась, и в дальнейшем обновлялась",
            reply_markup=await sub_keyboard(),
        )
        await state.set_state(BotState.subscribe)
