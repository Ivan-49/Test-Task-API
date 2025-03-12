from aiogram.fsm.state import StatesGroup, State


class BotState(StatesGroup):
    start = State()
    helping = State()

    resume = State()
    get_product = State()
    none_information = State()
    subscribe = State()
    user_sub = State()
    get_product_article = State()
    get_product_article_for_sub = State()
    wainting_article = State()
    AI_analysis = State()
    analog = State()
    last_time_data = State
