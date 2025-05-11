from abc import ABC, abstractmethod

from fastapi import Depends

from app.database import AsyncSessionLocal
from app.product_repository import ProductRepository
from app.product_service import ProductService
from app.schemas import ProductQuantityUpdate
from consumer.constants import BindEvent


class ProductEventHandler(ABC):
    """
    Abstract handler class
    """

    @abstractmethod
    async def handle(self, product_data: ProductQuantityUpdate):
        pass


class ProductSellingEventHandler(ProductEventHandler):
    """
    Handle product selling action
    """

    def __init__(self, product_service: ProductService):
        self.product_service = product_service

    async def handle(self, product_data: ProductQuantityUpdate):
        await self.product_service.sell_product(product_data)


class ProductRefundEventHandler(ProductEventHandler):
    """
    Handle product refund action
    """

    def __init__(self, product_service: ProductService = Depends(ProductService)):
        self.product_service = product_service

    async def handle(self, product_data: ProductQuantityUpdate):
        await self.product_service.refund_product(product_data)


class ProductHandlerRegister:
    handlers: dict[str, ProductEventHandler] = {}

    def add_handler(self, bind_event: BindEvent, handler: ProductEventHandler) -> None:
        self.handlers[bind_event.value] = handler

    def remove_handler(self, bind_event: BindEvent) -> None:
        self.handlers.pop(bind_event.value, None)


def get_product_event_register():
    db = AsyncSessionLocal()
    product_repository = ProductRepository(db)
    product_service = ProductService(product_repository)
    # Create and fulfill registry
    product_event_register = ProductHandlerRegister()
    product_event_register.add_handler(BindEvent.SOLD, ProductSellingEventHandler(product_service))
    product_event_register.add_handler(BindEvent.REFUND, ProductRefundEventHandler(product_service))
    return product_event_register
