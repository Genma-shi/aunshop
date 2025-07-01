from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Stationery
from .serializers import StationerySerializer, StationeryListSerializer

class StationeryViewSet(viewsets.ModelViewSet):
    queryset = Stationery.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == 'list':
            return StationeryListSerializer
        return StationerySerializer

class RecentStationeryListView(generics.ListAPIView):
    serializer_class = StationerySerializer

    def get_queryset(self):
        # Возвращаем последние 5 добавленных канцтоваров (можно поменять лимит)
        return Stationery.objects.order_by('-created_at')