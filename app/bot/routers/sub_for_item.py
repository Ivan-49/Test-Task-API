from aiogram import types, F
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os

from ..keyboards import (
    start_keyboard,
    item_keyboard,
    sub_keyboard,
    info_product_keyboard,
)
from ..states import BotState
from ...utils.data_base_communications.get_item import get_item
from ...schemas import Article
from ...utils.data_base_communications.add_to_items import add_to_subs
from ...database import async_session

router = Router()


@router.message(BotState.subscribe, F.text == "Да я хочу это сделать")
async def subscribe(message: types.Message, state: FSMContext):
    await message.answer("Продублируйте мне артикул товара за которым я должен следить")
    await state.set_state(BotState.get_product_article_for_sub)


@router.message(BotState.get_product_article_for_sub)
async def choice(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with async_session() as session:
            article = Article(article=message.text)
            article = article.model_dump().get("article")
            await add_to_subs(articul=article, session=session)

        await message.answer(
            f"""Ваш артикул: {message.text}
товар по этому артикулу появится в моей базе данных при очередном сборе, который происходит 2 раза в сутки""",
            reply_markup=await info_product_keyboard(),
        )
        await state.set_state(BotState.resume)
    else:
        await message.answer("введите корректный артикул")
        await state.set_state(BotState.get_product_article_for_sub)
