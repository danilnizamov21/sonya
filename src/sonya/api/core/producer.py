import json

import pika


def publish_task(queue_name: str, task: dict) -> None:

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(
        queue=queue_name, durable=True, arguments={"x-queue-type": "quorum"}
    )
    try:
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(task).encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=2, content_type="application/json"
            ),
        )
    finally:
        connection.close()
