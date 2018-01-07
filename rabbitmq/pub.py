#!/usr/bin/env python
"""Publisher for rabbitmq."""

import pika


def main():
    """Simple message."""
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.135.133', 5672, 'test', credentials))

    channel = connection.channel()

    channel.queue_declare(queue='test')
    channel.basic_publush(exchange='', routing_key='test', body='Hello world!')
    connection.close()


if __name__ == '__main__':
    main()
