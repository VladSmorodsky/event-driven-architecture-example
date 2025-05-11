from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence

from app.dependencies import get_db
from app.models import Product
from app.schemas import ProductCreate


class ProductRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_all_products(self) -> Sequence[Product]:
        result = await self.session.execute(select(Product))
        return result.scalars().all()

    async def find_all_by_id(self, ids: list[int]) -> Sequence[Product]:
        result = await self.session.execute(select(Product).where(Product.id.in_(ids)))
        return result.scalars().all()

    async def find_by_id(self, product_id: int) -> Product:
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        return result.scalars().one_or_none()

    async def update_product(self, updated_product: Product) -> Product:
        await self.session.commit()
        await self.session.refresh(updated_product)
        return updated_product
