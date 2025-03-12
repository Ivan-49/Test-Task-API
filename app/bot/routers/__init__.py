from .AI import router as AI_router
from .commands import router as commands_router
from .information import router as information_router
from .analog import router as analog_router
from .sub_for_item import router as sub_for_item_router
from .all_informatioans import router as all_informatioans
from .sub_from_user import router as sub_from_user_router

all_routers = [
    AI_router,
    commands_router,
    information_router,
    analog_router,
    sub_for_item_router,
    all_informatioans,
    sub_from_user_router,
]
