from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, async_engine, Base
from .shedule.shedule import main as shedule, tick
from .routers.products import router as products_router
from .routers.subscribe import router as subscribe_router
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


app = FastAPI()
app.include_router(products_router)
app.include_router(subscribe_router)

scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    scheduler.add_job(tick, "interval", minutes=1)
    scheduler.start()
    # asyncio.create_task(shedule())


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
