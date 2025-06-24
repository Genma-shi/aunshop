from django.urls import path
from .views import CartListView, CartAddView, CartRemoveView

urlpatterns = [
    path('', CartListView.as_view(), name='cart_list'),
    path('add/', CartAddView.as_view(), name='cart_add'),
    path('remove/<int:pk>/', CartRemoveView.as_view(), name='cart_remove'),
]