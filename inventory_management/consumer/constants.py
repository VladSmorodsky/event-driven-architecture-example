from enum import Enum

EXCHANGE_NAME = 'inventory'
PRODUCT_QUEUE_NAME = 'product'


class BindEvent(Enum):
    SOLD = f'{PRODUCT_QUEUE_NAME}.sold'
    REFUND = f'{PRODUCT_QUEUE_NAME}.refund'
