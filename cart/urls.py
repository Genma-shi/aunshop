from django.urls import path
from .views import CartListView, CartAddView, CartRemoveView , CartIncreaseView, CartDecreaseView

urlpatterns = [
    path('', CartListView.as_view(), name='cart_list'),
    path('add/', CartAddView.as_view(), name='cart_add'),
    path('remove/<int:pk>/', CartRemoveView.as_view(), name='cart_remove'),
    path('increase/<int:pk>/', CartIncreaseView.as_view(), name='cart_increase'),
    path('decrease/<int:pk>/', CartDecreaseView.as_view(), name='cart_decrease'),
]