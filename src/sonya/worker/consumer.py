import json
import sys

import pika

from sonya.worker.handles import handle_task


def callback(ch, method, properties, body):
    try:
        task = json.loads(body.decode())
        handle_task(task)
    except Exception:
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False,
        )
    else:
        ch.basic_ack(
            delivery_tag=method.delivery_tag,
        )


def main(queue_name: str) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(
        queue=queue_name, durable=True, arguments={"x-queue-type": "quorum"}
    )
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=False
    )

    print("exit press CTRL+C")
    channel.start_consuming()

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False,
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Укажи очередь: sonya.inspect или sonya.collect")

    main(sys.argv[1])
