from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os
import logging

from ..states import BotState
from ...utils.fetch_utils import fetch_gpt
from ...utils.data_base_communications.get_item import get_item

load_dotenv()  # Загружаем переменные окружения

GPT_TOKEN = os.getenv("GPT_TOKEN")

CONDITION = os.getenv("CONDITION")

logger = logging.getLogger(__name__)

router = Router()
@router.message(BotState.get_product_article, F.text == "Посмотреть AI Анализ товара")
async def get_product(message: types.Message, state: FSMContext):
    logger.info("Receiving request for AI Analysis")  # Логируем момент получения запроса
    try:
        # Получаем артикул из состояния
        article_data = await state.get_data()  # Теперь будет корректно
        article = article_data.get("artikul")
        logger.info(f"Article received: {article}")

        # Извлекаем элемент из базы данных
        item = await get_item(article, 28)
        if item:
            response = ""
            for i in item:
                date = i[5]
                price = i[3]
                count = i[4]
                rating = i[6]
                response += f"Дата: {date}\nЦена: {price}\nКоличество: {count}\nРейтинга: {rating}\n\n"

            name = i[1]
            artikul = i[0]
            data = f"Название: {name}\nАртикул: {artikul}\n\n{response}"

            answer = await fetch_gpt(CHAD_API_KEY=GPT_TOKEN, request=data, condition=CONDITION)
            await message.answer(answer)
            await message.answer("Теперь вы можете сделать что-то с следующим товаром, просто скиньте мне новый артикул.")
            await state.set_state(BotState.wainting_article)
        else:
            await message.answer("Товар не найден.")  # Обработка отсутствия товара
    except Exception as e:
        logger.error(f"Error in get_product: {e}", exc_info=True)
        await message.answer("Произошла ошибка, пожалуйста, попробуйте позже.")