from fastapi import FastAPI
from app.routers import products, subscribe
from app.database import engine, Base


app = FastAPI()

app.include_router(products.router)
app.include_router(subscribe.router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Wildberries API"}