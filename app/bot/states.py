from aiogram.fsm.state import StatesGroup, State


class BotState(StatesGroup):
    start = State()
    get_product= State()
    subscribe = State()

class ProductForm(StatesGroup):
    product_article = State()
