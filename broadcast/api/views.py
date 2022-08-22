from rest_framework import viewsets, permissions, filters

from broadcast.api.serializers import BroadcastSerializer
from broadcast.models import Broadcast


class BroadcastViewSet(viewsets.ModelViewSet):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags__title']

