from rest_framework import serializers as rest_serializers
from rest_framework_mongoengine import serializers

from broadcast.models import Broadcast
from utils import clean_search


class BroadcastSerializer(serializers.DocumentSerializer):
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
