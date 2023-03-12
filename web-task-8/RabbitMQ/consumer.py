import pika

import time
import json
from mock.models import Contact
import mock.connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='message', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def sending_message(message: dict):
    contacts = Contact.objects(id__exact=message['id'])
    for contact in contacts:
        contact.update(logic_field=True)
        print(f'The message {message} was sent to the address {contact.email}')


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    sending_message(message)
    time.sleep(1)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='message', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
