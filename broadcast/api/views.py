import random

from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from broadcast.api.serializers import BroadcastSerializer, SearchSerializer, FileSerializer
from broadcast.models import Broadcast
from utils import number_and_size, get_response


class BroadcastViewSet(viewsets.ModelViewSet):
    queryset = Broadcast.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'search':
            return SearchSerializer
        return BroadcastSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.getlist('attached_files')
        print(file)
        urls = []
        base_url = self.request.build_absolute_uri('/')
        for f in file:
            data = {'file': f}
            serializer = FileSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            file_url = serializer.data['file']

            urls.append(base_url + file_url)
        data = {
            'title': request.data['title'],
            'description': request.data['description'],
            'attached_files': urls,
            'tags': request.data.getlist('tags')
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        files = request.FILES.getlist('attached_files')
        urls = []
        base_url = self.request.build_absolute_uri('/')
        for f in files:
            data = {'file': f}
            serializer = FileSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            file_url = serializer.data['file']

            urls.append(base_url + file_url)
        data = {
            'title': request.data['title'],
            'description': request.data['description'],
            'attached_files': urls,
            'tags': request.data.getlist('tags')
        }
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def paginate_queryset(self, queryset):
        page_number, page_size = number_and_size(self.request)
        return queryset.skip((page_number - 1) * page_size).limit(page_size)

    def get_paginated_response(self, data, count=None):
        if count is None:
            count = self.queryset.count()
        response = get_response(self.request, data, count)
        return Response(response)

    @action(detail=False, methods=['GET'])
    def search(self, request):
        page_number, page_size = number_and_size(self.request)
        search_text = request.query_params.get('search_text', '0')
        serializer = self.get_serializer(data={'search_text': search_text})
        serializer.is_valid(raise_exception=True)
        cleaned_search_text = serializer.validated_data['search_text']
        print(cleaned_search_text)
        # query = search_to_query(cleaned_search_text)
        queryset = Broadcast.objects.search_text(' '.join(cleaned_search_text)).order_by('$text_score')
        queryset = queryset.skip(page_number - 1).limit(page_size)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = BroadcastSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data, count=queryset.count())


