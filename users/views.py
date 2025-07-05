from rest_framework import generics, status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, FCMTokenSerializer
from .jwt_serializers import PhoneTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from .models import EmailConfirmationCode
import random

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        user = authenticate(request, username=phone, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class FCMTokenView(APIView):
    serializer_class = FCMTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FCMTokenSerializer(data=request.data)
        if serializer.is_valid():
            request.user.fcm_token = serializer.validated_data['fcm_token']
            request.user.save()
            return Response({"message": "FCM token updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class = PhoneTokenObtainPairSerializer

class SendEmailConfirmationCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required"}, status=400)

        code = str(random.randint(100000, 999999))
        EmailConfirmationCode.objects.create(user=request.user, email=email, code=code)

        send_mail(
            'Подтверждение Email',
            f'Ваш код подтверждения: {code}',
            'genmashi150505@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Код отправлен на email"})

class ConfirmEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        confirmation = EmailConfirmationCode.objects.filter(user=request.user, email=email, code=code).first()
        if confirmation:
            confirmation.is_confirmed = True
            confirmation.save()

            request.user.email = email
            request.user.save()
            return Response({"message": "Email подтверждён"})
        return Response({"error": "Неверный код"}, status=400)

class SendPasswordResetCodeView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required"}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Пользователь с таким email не найден"}, status=404)

        code = str(random.randint(100000, 999999))
        EmailConfirmationCode.objects.create(user=user, email=email, code=code)

        send_mail(
            'Сброс пароля',
            f'Ваш код сброса пароля: {code}',
            'genmashi150505@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Код отправлен на email"})
class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        password1 = request.data.get("password")
        password2 = request.data.get("password2")

        if password1 != password2:
            return Response({"error": "Пароли не совпадают"}, status=400)

        confirmation = EmailConfirmationCode.objects.filter(email=email, code=code).first()
        if not confirmation:
            return Response({"error": "Неверный код"}, status=400)

        user = confirmation.user
        user.set_password(password1)
        user.save()
        confirmation.delete()
        return Response({"message": "Пароль успешно сброшен"})
