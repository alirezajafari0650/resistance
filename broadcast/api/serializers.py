from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from broadcast.models import AttachedFile, Broadcast, Tag


class AttachedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachedFile
        fields = ['id', 'broadcast', 'file', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title', 'created_at']


class BroadcastSerializer(WritableNestedModelSerializer):
    attached_files = AttachedFileSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Broadcast
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'tags', 'attached_files']
