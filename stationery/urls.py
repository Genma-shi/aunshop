from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationeryViewSet , RecentStationeryListView

router = DefaultRouter()
router.register(r'items', StationeryViewSet, basename='stationery')

urlpatterns = [
    path('', include(router.urls)),
    path('recent/', RecentStationeryListView.as_view(), name='stationery_recent'),
]