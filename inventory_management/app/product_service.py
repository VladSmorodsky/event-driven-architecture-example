from fastapi import Depends, HTTPException
from sqlalchemy import Sequence

from app.models import Product
from app.product_repository import ProductRepository
from app.schemas import ProductCreate, ProductQuantityUpdate


class ProductService:
    def __init__(self, product_repository: ProductRepository = Depends()):
        self.product_repository = product_repository

    async def create_product(self, product_data: ProductCreate) -> Product:
        return await self.product_repository.create_product(product_data)

    async def get_all_products(self) -> Sequence[Product]:
        return await self.product_repository.get_all_products()

    async def sell_product(self, products_data: ProductQuantityUpdate):
        product = await self.product_repository.find_by_id(products_data.id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.quantity -= products_data.quantity
        await self.product_repository.update_product(product)

    async def refund_product(self, products_data: ProductQuantityUpdate):
        product = await self.product_repository.find_by_id(products_data.id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.quantity += products_data.quantity
        await self.product_repository.update_product(product)
