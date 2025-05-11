import json
from contextlib import asynccontextmanager

from aio_pika import connect, ExchangeType, DeliveryMode, Message
from fastapi import FastAPI

from settings import RABBITMQ_URL

INVENTORY_EXCHANGE_NAME = 'inventory'

app = FastAPI()


async def get_connection():
    return await connect(RABBITMQ_URL)


@app.post('/orders/{order_id}/pay')
async def pay_order(order_id: int):
    connection = await get_connection()
    channel = await connection.channel()
    exchange = await channel.declare_exchange(INVENTORY_EXCHANGE_NAME, ExchangeType.TOPIC, durable=True)

    # Emulates sending order item
    product = {"id": 1, "quantity": 2}

    message = Message(json.dumps(product).encode('utf-8'), delivery_mode=DeliveryMode.PERSISTENT,
                      content_type="application/json", )

    await exchange.publish(
        message=message,
        routing_key="product.sold",
    )

    await connection.close()
    return product


@app.post('/orders/{order_id}/refund')
async def refund_order(order_id: int):
    connection = await get_connection()
    channel = await connection.channel()
    exchange = await channel.declare_exchange(INVENTORY_EXCHANGE_NAME, ExchangeType.TOPIC, durable=True)

    # Emulates sending order item
    product = {"id": 1, "quantity": 2}

    message = Message(json.dumps(product).encode('utf-8'), delivery_mode=DeliveryMode.PERSISTENT,
                      content_type="application/json", )

    await exchange.publish(
        message=message,
        routing_key="product.refund",
    )

    await connection.close()
    return product
