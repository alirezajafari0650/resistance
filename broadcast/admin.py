from django.contrib import admin
from broadcast.models import Broadcast, AttachedFile, Tag
admin.site.register(Broadcast)
admin.site.register(AttachedFile)
admin.site.register(Tag)
