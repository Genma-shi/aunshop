from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # добавляем доп. инфу в payload
        token['phone_number'] = user.phone_number
        token['full_name'] = f"{user.first_name} {user.last_name}"
        return token

    def validate(self, attrs):
        # заменим username на phone_number
        self.user = self.context['request'].user
        attrs['username'] = attrs.get('phone_number')
        return super().validate(attrs)
