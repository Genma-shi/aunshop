from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .models import Stationery , Category
from .serializers import StationerySerializer, StationeryListSerializer , CategorySerializer
from rest_framework import generics

class StationeryViewSet(viewsets.ModelViewSet):
    queryset = Stationery.objects.all()
    permission_classes = [AllowAny]
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
        return Stationery.objects.order_by('-created_at')[:10]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]