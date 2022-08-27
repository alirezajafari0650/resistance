from datetime import datetime

from djongo import models
from mongoengine import connect, Document, fields

connect('local')


class File(models.Model):
    file = models.FileField(upload_to='files/')


class Broadcast(Document):
    title = fields.StringField(max_length=100, required=True)
    description = fields.StringField(max_length=1000, required=True)
    attached_files = fields.ListField(fields.URLField())
    created_at = fields.DateTimeField(default=datetime.now)
    tags = fields.ListField(fields.StringField(max_length=100))
    is_story = fields.BooleanField(default=False)

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
