from aiogram import F, types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from ..keyboards import *
from ..states import BotState

load_dotenv()

router = Router()


@router.message(
    BotState.get_product_article, F.text == "Подписаться на обновление данных о товаре"
)
async def subscribe_user(message: types.Message, state: FSMContext):
    await message.answer(
        "Пока эта функция не работает, но скоро будет, так что скиньте мне артикул еще раз и посомтри другие функции",
        reply_markup=await sub_keyboard(),
    )
    await state.set_state(BotState.wainting_article)
