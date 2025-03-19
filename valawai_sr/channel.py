from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from valawai_sr.config import env
from valawai_sr.messages import BaseMessage


class Channel:
    _channel: BlockingChannel

    def __init__(self, channel: BlockingChannel = None) -> None:
        """Get a channel from the configured host address."""
        if channel is None:
            connection = BlockingConnection(ConnectionParameters(host=env.rmq_host))
            channel = connection.channel()
        self._channel = channel

    def configure_consume(
        self,
        key: str,
        on_message,
        queue: str = "",
    ) -> BlockingChannel:
        """Configure consume with a queue on the configured exchange with the given key."""
        # If queue is an empty string, a new queue is created with a random name
        queue = self._channel.queue_declare(queue).method.queue

        self._channel.queue_bind(queue, env.exchange, key)
        self._channel.basic_consume(queue, on_message, True)

    def publish(self, key: str, message: BaseMessage) -> None:
        """Publish message to configured exchange with give key."""
        body = message.to_json()
        self._channel.basic_publish(env.exchange, key, body)

    def start_consuming(self) -> None:
        self._channel.start_consuming()
