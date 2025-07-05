from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('fcm-token/', FCMTokenView.as_view(), name='fcm-token'),
    path('token/', PhoneTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('email/send-code/', SendEmailConfirmationCodeView.as_view()),
    path('email/confirm/', ConfirmEmailView.as_view()),

    path('password/send-code/', SendPasswordResetCodeView.as_view()),
    path('password/reset/', ResetPasswordView.as_view()),
]
