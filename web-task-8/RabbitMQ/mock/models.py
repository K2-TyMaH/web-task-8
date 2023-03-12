from mongoengine import Document
from mongoengine.fields import StringField, EmailField, BooleanField


class Contact(Document):
    fullname = StringField()
    email = EmailField()
    logic_field = BooleanField()
