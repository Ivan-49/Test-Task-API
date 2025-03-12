from aiogram import types, F
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os
import logging

from ...database import async_session
from ..keyboards import start_keyboard, item_keyboard, sub_keyboard
from ..states import BotState
from ...utils.data_base_communications.get_item import get_item
from ...utils.fetch_utils import fetch_product_details
from ...schemas import Product
from ...utils.data_base_communications.add_to_items import add_to_items, add_to_subs


load_dotenv()


router = Router()
logger = logging.getLogger(__name__)

load_dotenv()  # Загружаем переменные окружения

RELATED_TEXT = os.getenv("RELATED_TEXT")


@router.message(BotState.resume, F.text == "Продолжить")
async def next(message: types.Message, state: FSMContext):
    await state.set_state(BotState.get_product)


@router.message(BotState.resume, F.text == "Закончить")
async def stop(message: types.Message, state: FSMContext):
    await message.answer(
        "Приятно было пообщаться)", reply_markup=await start_keyboard()
    )
    await state.set_state(BotState.start)


@router.message(BotState.resume, F.text == "Узнать информацию о товаре")
async def get_article(message: types.Message, state: FSMContext):
    await message.answer("Введите артикул нужного вам товара:")
    await state.set_state(BotState.wainting_article)


@router.message(BotState.wainting_article)
async def choice(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer(
            "ваш артикул: " + message.text + "\n" + "Что вы хотите сделать?",
            reply_markup=await item_keyboard(),
        )
        await state.update_data(artikul=message.text)
        await state.set_state(BotState.get_product_article)
    else:
        await message.answer("введите корректный артикул")
        await state.set_state(BotState.wainting_article)


@router.message(BotState.get_product_article, F.text == "Получить информацию о товаре")
async def get_product(message: types.Message, state: FSMContext):
    article = await state.get_data()
    article = article.get("artikul")

    result = await fetch_product_details(article)

    try:
        async with async_session() as session:
            if not isinstance(result.get("artikul"), str):
                result["artikul"] = str(result.get("artikul"))
            result["date_time"] = result["date_time"].replace(tzinfo=None)

            details = Product(**result)
            details = details.model_dump()

            await add_to_items(details, session=session)
            await add_to_subs(article, session=session)

    except Exception as e:
        logger.exception(f"Error processing product: {e}")

    item = await get_item(article, 1)
    if item:
        await message.answer(
            f"Название: {item[1]}\n"
            + f"Артикул: {item[0]}\n"
            + f"Цена: {item[3]}\n"
            + f"Количество: {item[4]}\n"
            + f"Дата обновления данных о товаре: {item[5]}\n"
            + f"Рейтинг: {item[6]}"
        )
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
