from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Stationery
from .serializers import StationerySerializer

class StationeryListView(generics.ListAPIView):
    queryset = Stationery.objects.all()
    serializer_class = StationerySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'brand']

class StationeryDetailView(generics.RetrieveAPIView):
    queryset = Stationery.objects.all()
    serializer_class = StationerySerializer