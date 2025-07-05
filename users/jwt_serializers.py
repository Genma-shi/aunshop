from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone_number'] = user.phone_number
        token['full_name'] = f"{user.first_name} {user.last_name}"
        return token

    def validate(self, attrs):
        print("attrs before:", attrs)
<<<<<<< HEAD
        attrs['username'] = attrs['phone_number']  # подменяем username для аутентификации
=======
        attrs['username'] = attrs['phone_number']  # пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ username пїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
>>>>>>> d27e09a2c0be8f10faa03f7cadeb3f330d7b5baa
        print("attrs after:", attrs)
        return super().validate(attrs)
