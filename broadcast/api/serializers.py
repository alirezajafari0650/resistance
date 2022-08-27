from rest_framework import serializers as rest_serializers
from rest_framework_mongoengine import serializers

from broadcast.models import Broadcast, File
from utils import clean_search


class FileSerializer(rest_serializers.ModelSerializer):
    file = rest_serializers.FileField()

    class Meta:
        model = File
        fields = '__all__'

    def validate_file(self, file):
        if file.name.split('.')[-1] not in ['jpg', 'png', 'jpeg', 'mp4']:
            raise rest_serializers.ValidationError('فایل ضمیمه باید عکس یا فیلم باشد')
        elif file.size > 50000000:
            raise rest_serializers.ValidationError('فایل ضمیمه باید کوچکتر از 50 مگابایت باشد')
        return file


class BroadcastSerializer(serializers.DocumentSerializer):
    attached_files = rest_serializers.ListField(child=rest_serializers.URLField())

    class Meta:
        model = Broadcast
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class SearchSerializer(rest_serializers.Serializer):
    search_text = rest_serializers.CharField(max_length=100)

    @staticmethod
    def validate_search_text(value):
        if type(value) == str:
            if len(value) < 3:
                raise rest_serializers.ValidationError('متن سرچ باید حداقل سه کاراکتر باشد')
            elif len(value) > 100:
                raise rest_serializers.ValidationError('متن سرچ باید حداکثر صد کاراکتر باشد')
            else:
                return clean_search(value)
        else:
            raise rest_serializers.ValidationError('متن سرچ نامعتبر است')
