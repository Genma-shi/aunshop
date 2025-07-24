from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import GlobalSearchView , PageContentDetailView , ContactPhoneNumberView , test_push

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),

    path('test-push/', test_push),

    # API
    path('api/', include(router.urls)),
    path('api/', include('users.urls')),
    path('api/books/', include('books.urls')),
    path('api/stationery/', include('stationery.urls')),
    path('api/promotions/', include('promotions.urls')),
    path('api/cart/', include('cart.urls')),

    path('whatsapp-phone/', ContactPhoneNumberView.as_view(), name='whatsapp_phone'),
    path('api/page-content/<str:key>/', PageContentDetailView.as_view(), name='page-content-detail'),

    path('search/', GlobalSearchView.as_view(), name='global-search'),
    # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
