from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("PhoneBackend.authenticate called with:", username, password)
        if username is None or password is None:
            return None
        try:
            user = UserModel.objects.get(phone_number=username)
        except UserModel.DoesNotExist:
            print("User not found")
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            print("Authentication success")
            return user
        print("Authentication failed")
        return None
