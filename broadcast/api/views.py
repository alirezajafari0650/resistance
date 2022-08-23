import re

from django.db.models import Q
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from broadcast.api.serializers import BroadcastSerializer, AttachedFileSerializer
from broadcast.models import Broadcast, AttachedFile


class BroadcastViewSet(viewsets.ModelViewSet):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags__title']

    @staticmethod
    def reverse_number(text):
        list_text = []
        persian_numbers = {
            '۰': '0',
            '۱': '1',
            '۲': '2',
            '۳': '3',
            '۴': '4',
            '۵': '5',
            '۶': '6',
            '۷': '7',
            '۸': '8',
            '۹': '9',
        }
        english_numbers = {
            '0': '۰',
            '1': '۱',
            '2': '۲',
            '3': '۳',
            '4': '۴',
            '5': '۵',
            '6': '۶',
            '7': '۷',
            '8': '۸',
            '9': '۹',
        }
        for i in range(len(text)):
            if text[i] in persian_numbers:
                if len(text[i - 1]) > 2:
                    list_text.append(' '.join([text[i - 1], persian_numbers[text[i]]]))
                elif len(text[i + 1]) > 2:
                    list_text.append(' '.join([persian_numbers[text[i]], text[i + 1]]))
            elif text[i] in english_numbers:
                if len(text[i - 1]) > 2:
                    list_text.append(' '.join([text[i - 1], english_numbers[text[i]]]))
                elif len(text[i + 1]) > 2:
                    list_text.append(' '.join([english_numbers[text[i]], text[i + 1]]))

        return list_text

    @action(detail=False, methods=['POST'])
    def search(self, request):
        """
        Full text search for broadcasts
        """
        search_text = request.data.get('search_text')
        if len(search_text) < 3:
            return Response({'error': 'متن سرچ باید حداقل سه کاراکتر باشد'})
        elif len(search_text) > 100:
            return Response({'error': 'متن سرچ باید کمتر از 100 کاراکتر باشد'})
        if search_text:
            search_text = re.split(' |\u200c|,|;|،|\n', search_text)
            search_text.extend(self.reverse_number(search_text))
            search_text = list(set(search_text))
            cleaned_search_text = []
            for text in search_text:
                if len(text) > 2 and (not text.isdigit()):
                    cleaned_search_text.append(text)
            queryset = []
            print(cleaned_search_text)
            for item in cleaned_search_text:
                queryset += Broadcast.objects.filter(
                    Q(title__icontains=item) |
                    Q(description__icontains=item) |
                    Q(tags__title__icontains=item)
                )
            serializer = BroadcastSerializer(list(set(queryset)), many=True)
            return Response(serializer.data)

        return Response({'search_text': 'متن سرچ نامعتبر است'})


class AttachedFileViewSet(viewsets.ModelViewSet):
    queryset = AttachedFile.objects.all()
    serializer_class = AttachedFileSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags__title']
