from rest_framework import generics, status , permissions
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, FCMTokenSerializer , NotificationSettingSerializer , PasswordResetCodeSerializer, CheckResetCodeSerializer, SetNewPasswordSerializer , AddressSerializer	
from .jwt_serializers import PhoneTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from .models import EmailConfirmationCode
import random 
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException  # <-- правильно

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
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email обязателен"}, status=400)

        code = str(random.randint(100000, 999999))

        # Удаляем старые коды с этим email
        EmailConfirmationCode.objects.filter(email=email).delete()

        # Создаём новый код
        EmailConfirmationCode.objects.create(email=email, code=code, is_confirmed=False)

        send_mail(
            'Код подтверждения email',
            f'Ваш код: {code}',
            'genmashi150505@gmail.com',
            [email]
        )

        return Response({"message": "Код отправлен"})

class ConfirmEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        confirmation = EmailConfirmationCode.objects.filter(
            email=email, code=code
        ).first()

        if not confirmation:
            return Response({"error": "Неверный код"}, status=400)

        confirmation.is_confirmed = True
        confirmation.save()

        return Response({"message": "Email подтверждён"})

class SendPasswordResetCodeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetCodeSerializer

    def post(self, request):
        try:
            print("📥 Данные запроса:", request.data)
 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                print("❌ Ошибка валидации:", serializer.errors)
                return Response(serializer.errors, status=400)

            email = serializer.validated_data['email']
            print("📧 Email:", email)

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"detail": "Пользователь с таким email не найден"}, status=404)

            code = str(random.randint(100000, 999999))
            EmailConfirmationCode.objects.filter(email=email).delete()
            EmailConfirmationCode.objects.create(email=email, code=code, is_confirmed=False)

            try:
                send_mail(
                    'Сброс пароля',
                    f'Ваш код сброса пароля: {code}',
                    'genmashi150505@gmail.com',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                print("❌ Ошибка при отправке письма:", str(e))
                return Response({"error": "Ошибка при отправке письма"}, status=500)

            print("✅ Код отправлен на почту")
            return Response({"message": "Код отправлен на email"})

        except Exception as e:
            print("🔥 Общая ошибка:", str(e))
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=500)

# Этап 1: проверка кода
class CheckPasswordResetCodeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CheckResetCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        confirmation = EmailConfirmationCode.objects.filter(
            email=email,
            code=code,
            is_confirmed=False
        ).first()

        if not confirmation:
            return Response({"error": "Неверный код"}, status=400)

        confirmation.is_confirmed = True
        confirmation.save()

        return Response({"message": "Код подтверждён. Теперь можно задать новый пароль."})

# Этап 2: установка нового пароля
class SetNewPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password1 = serializer.validated_data['password']
        password2 = serializer.validated_data['password2']

        if password1 != password2:
            return Response({"error": "Пароли не совпадают"}, status=400)

        confirmation = EmailConfirmationCode.objects.filter(
            email=email,
            is_confirmed=True
        ).order_by('-created_at').first()

        if not confirmation:
            return Response({"error": "Сначала подтвердите код"}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=404)

        user.set_password(password1)
        user.save()
        confirmation.delete()

        return Response({"message": "Пароль успешно установлен"})

class AddressUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            request.user.address = serializer.validated_data['address']
            request.user.save()
            return Response({"message": "Адрес успешно обновлён"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"address": request.user.address or ""})


class NotificationSettingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'notifications_enabled': request.user.notifications_enabled})

    def post(self, request):
        serializer = NotificationSettingSerializer(data=request.data)
        if serializer.is_valid():
            request.user.notifications_enabled = serializer.validated_data['notifications_enabled']
            request.user.save()
            return Response({'notifications_enabled': request.user.notifications_enabled})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)