from logging import getLogger
from aiogram import types, F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from ...utils.data_base_communications.get_item import get_item_by_name
from ..conf import COUNT_ANALOG
from ..keyboards import sub_keyboard
from ..states import BotState
from ...utils.data_base_communications.get_item import get_item
from ...utils.fetch_utils import fetch_product_details
from ...schemas import Product
from ...utils.data_base_communications.add_to_items import add_to_items, add_to_subs




logger = getLogger(__name__)

load_dotenv()

router = Router()

@router.message(BotState.get_product_article, F.text == "Посмотреть аналоги")
async def analog_items(message: types.Message, state: FSMContext):


    result = ""
    articul = (await state.get_data()).get("artikul")
    product = await fetch_product_details(articul)

    if not isinstance(product.get("artikul"), str):
        product["artikul"] = str(product.get("artikul"))
    product["date_time"] = product["date_time"].replace(tzinfo=None)

    details = Product(**product)
    details = details.model_dump()

    await add_to_items(details)
    await add_to_subs(articul)

    item = await get_item((await state.get_data()).get("artikul"), 1)
    logger.error(item)
    if item is None:
        await message.answer(
            "К сожалению, товар с таким артикулом не найден в нашей базе данных.",
            reply_markup=await sub_keyboard(),  # Или другая клавиатура по необходимости
        )
        await state.set_state(BotState.wainting_article)  # Возвращаемся к ожиданию артикула
        return  # Прерываем выполнение функции, чтобы избежать ошибки

    name = item[1]  # Теперь мы уверены, что item не None
    analogs = await get_item_by_name(name=name, count=COUNT_ANALOG)
    if analogs is not None and len(analogs) > 0:
        for index, analog in enumerate(analogs):
            if analog[0] == articul:
                continue
            prores = f"""Аналог {index+1}.
Артикул: {analog[0]}
Название: {analog[1]}
Дата обновления данных: {analog[5]}
Цена: {analog[3]}
Количество на складе: {analog[4]}
Рейтинг товара: {analog[6]}
"""
            result += prores

        await message.answer(text=result)
        await message.answer(
            "Теперь вы можете сделать что то с следющим товаром, просто скинте мне новый артикул"
        )
        await state.set_state(BotState.wainting_article)
    else:
        await message.answer(
            "Мы ищем аналоги вашего товара, в нашей базе даннх, нов ней на данный момент нет ни одного аналога для вашего товара.Что бы аналоги начали появляться мне нужно больше времени и больший охват пользователей, извините)",
            reply_markup=await sub_keyboard(),
        )
        await state.set_state(BotState.subscribe)