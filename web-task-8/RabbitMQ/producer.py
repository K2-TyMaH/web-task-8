import json

import pika
from faker import Faker

from mock.models import Contact
import mock.connect


fake = Faker('uk_UA')
NUMBER_OF_CONTACTS = 9


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.exchange_declare(exchange='sending', exchange_type='direct')
channel.queue_declare(queue='message', durable=True)
channel.queue_bind(exchange='sending', queue='message')


def upload_contacts_to_the_database():
    """Upload contacts to database."""
    email = fake.email()
    Contact(
        fullname=fake.name(),
        email=email,
        logic_field=False,
        ).save()
    author_id = Contact.objects(email__exact=email).first().id
    return str(author_id)


def main():
    for i in range(NUMBER_OF_CONTACTS):
        message = {"id": upload_contacts_to_the_database()}

        channel.basic_publish(
            exchange='sending',
            routing_key='message',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    main()
