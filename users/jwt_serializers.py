from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField(write_only=True)

    username_field = 'phone_number'  # ВАЖНО: сообщаем базовому классу, что логин — phone_number

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone_number'] = user.phone_number
        token['full_name'] = f"{user.first_name} {user.last_name}"
        return token

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        if not phone_number:
            raise serializers.ValidationError('Phone number is required')

        # Подставляем phone_number как username_field
        attrs[self.username_field] = phone_number
        # attrs.pop('phone_number', None)

        return super().validate(attrs)
