from django.urls import path
from .views import StationeryListView, StationeryDetailView

urlpatterns = [
    path('', StationeryListView.as_view(), name='stationery_list'),
    path('<int:pk>/', StationeryDetailView.as_view(), name='stationery_detail'),
]