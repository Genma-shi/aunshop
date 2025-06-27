from rest_framework import generics, filters , viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Stationery
from .serializers import StationerySerializer
from rest_framework.filters import SearchFilter

class StationeryListView(generics.ListAPIView):
    queryset = Stationery.objects.all()
    serializer_class = StationerySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'brand']

class StationeryDetailView(generics.RetrieveAPIView):
    queryset = Stationery.objects.all()
    serializer_class = StationerySerializer

class StationeryViewSet(viewsets.ModelViewSet):
    queryset = Stationery.objects.all()
    serializer_class = StationerySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']  # Фильтрация по категории
    search_fields = ['title']  # Поиск по названию