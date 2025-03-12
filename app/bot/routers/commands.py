from aiogram import types, F
from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.fsm.context import FSMContext

from ..keyboards import helper_keyboard, info_product_keyboard
from ..states import BotState
from ..conf import HELP_TEXT, RELATED_TEXT


router = Router()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer(RELATED_TEXT, reply_markup=await info_product_keyboard())
    await state.set_state(BotState.resume)


@router.message(Command("help"))
async def help(message: types.Message, state: FSMContext):
    await message.answer(HELP_TEXT)
    await state.set_state(BotState.helping)


@router.message(BotState.helping)
async def resume(message: types.Message, state: FSMContext):
    await message.answer("Начнем работу?", reply_markup=await helper_keyboard())
    await state.set_state(BotState.resume)
