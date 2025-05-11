from contextlib import asynccontextmanager

from fastapi import FastAPI, status, Depends

from app.database import engine, Base
from app.product_service import ProductService
from app.schemas import ProductCreate

RABBIT_HOST = 'rabbitmq'
QUEUE_NAME = 'task_queue'


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.post('/products', status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, product_service: ProductService = Depends()):
    return await product_service.create_product(product_data)


@app.get('/products', status_code=status.HTTP_200_OK)
async def get_products(product_service: ProductService = Depends()):
    return await product_service.get_all_products()
