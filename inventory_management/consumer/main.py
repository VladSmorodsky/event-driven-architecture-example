import asyncio
import json
import os

from aio_pika import connect, ExchangeType
from aio_pika.abc import AbstractIncomingMessage

from app.schemas import ProductQuantityUpdate
from consumer.constants import EXCHANGE_NAME, PRODUCT_QUEUE_NAME, BindEvent
from consumer.handlers import get_product_event_register


async def on_message(message: AbstractIncomingMessage):
    data = json.loads(message.body.decode("utf-8"))
    product_data = ProductQuantityUpdate(**data)
    product_event_register = get_product_event_register()
    await product_event_register.handlers[message.routing_key].handle(product_data)
    print(f"[x] Retrieve message: data={product_data} key={message.routing_key}")


async def main():
    conn = await connect(host=os.getenv('RABBITMQ_URL'))
    channel = await conn.channel()
    inventory_exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.TOPIC, durable=True)
    queue = await channel.declare_queue(PRODUCT_QUEUE_NAME, durable=True)
    await queue.bind(inventory_exchange, routing_key=f"{BindEvent.SOLD.value}")
    await queue.bind(inventory_exchange, routing_key=f"{BindEvent.REFUND.value}")
    await queue.consume(on_message)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    # keep the loop running
    await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
