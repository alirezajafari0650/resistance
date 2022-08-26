# from djongo import models
# from django.db import models
from datetime import datetime

from mongoengine import connect, Document, fields

from utils import upload_broadcast

connect('local')


class Broadcast(Document):
    title = fields.StringField(max_length=100, required=True)
    description = fields.StringField(max_length=1000, required=True)
    attached_files = fields.ListField(fields.FileField(upload_to=upload_broadcast), required=False)
    created_at = fields.DateTimeField(default=datetime.now)
    tags = fields.ListField(fields.StringField(max_length=100))

    meta = {
        'ordering': ['-created_at'],
        'indexes': [
            {'fields': ['$title', '$description', '$tags'],
             'weights': {'tags': 10, 'title': 5, 'description': 1}
             }
        ]
    }

    def __str__(self):
        return self.title
