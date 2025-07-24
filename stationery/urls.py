from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationeryViewSet , RecentStationeryListView , CategoryViewSet

router = DefaultRouter()
router.register(r'items', StationeryViewSet, basename='stationery')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('recent/', RecentStationeryListView.as_view(), name='stationery_recent'),
]
