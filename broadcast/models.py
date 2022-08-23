from djongo import models
from broadcast.utils import upload_broadcast


class Broadcast(models.Model):
    """
    Broadcast model
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title


class AttachedFile(models.Model):
    """
    Attached file model
    """
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE, related_name='attached_files')
    file = models.FileField(upload_to=upload_broadcast)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name + ' - ' + self.broadcast.title


class Tag(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
