# event-driven-architecture-example

This project emulates microservice communication between two services.
It consists of:

- `order_management` service - emulates sending messages of selling and refund product
- `inventory_management` service - receives messages and updates product quantity (reduce when product is sold and
  increase when it is refunded).

## Setup

1. Clone the repo
2. Go to `order_management` directory and create `.env` file from `.env.example` and set values:
    - **`DB_NAME`**: database name.
    - **`DB_USER`**: database user.
    - **`DB_PASSWORD`**: database user password.
    - **`DB_HOST`**: database host.
    - **`DB_PORT`**: database port.
    - **`DB_URL`**: connection string with next template:
      `<dialect>+<async_version>://<user>:<password>@<host>:<port>/<database_name>`.
    - **`RABBITMQ_URL`**: connection string for RabbitMQ with next template: `amqp://<user>:<password>@<host>:<port>`
3. Create a docker network for communicating with RabbitMQ:
    ```shell
    docker network create rabbitmq-network
    ```
4. Run docker compose file in `order_management` directory:
    ```shell
    docker compose up --build -d
    ```
5. Go to `order_management` directory and create `.env` file from `.env.example` and set values:
    - **`DB_NAME`**: database name.
    - **`DB_USER`**: database user.
    - **`DB_PASSWORD`**: database user password.
    - **`DB_HOST`**: database host.
    - **`DB_PORT`**: database port.
    - **`DB_URL`**: connection string with next template:
      `<dialect>+<async_version>://<user>:<password>@<host>:<port>/<database_name>`.
    - **`RABBITMQ_URL`**: connection string for RabbitMQ with next template: `amqp://<user>:<password>@<host>:<port>`
6. Run docker compose file `order_management` directory:
    ```shell
    docker compose up --build -d
    ```