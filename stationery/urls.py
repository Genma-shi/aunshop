from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationeryViewSet

router = DefaultRouter()
router.register(r'', StationeryViewSet, basename='stationery')

urlpatterns = [
    path('', include(router.urls)),
]