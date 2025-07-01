from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from stationery.views import StationeryViewSet
from books.views import BookViewSet
from promotions.views import PromotionListView, PromotionDetailView

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API маршруты
    path('api/', include(router.urls)),
    path('api/', include('users.urls')),
    path('api/books/', include('books.urls')),
    path('api/stationery/', include('stationery.urls')),
    path('api/promotions/', include('promotions.urls')),
    path('api/cart/', include('cart.urls')),

    # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
