from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .routers.products import router as products_router
from .routers.subscribe import router as subscribe_router
from .database import async_engine, Base
from .shedule.shedule import tick
import logging

logger = logging.getLogger("sqlalchemy")
logger.setLevel(logging.INFO)


app = FastAPI()
app.include_router(products_router)
app.include_router(subscribe_router)

scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    scheduler.add_job(tick, "interval", seconds=10)
    scheduler.start()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=80, reload=True)
