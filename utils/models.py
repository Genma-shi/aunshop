from fcm_django.models import FCMDevice as BaseFCMDevice
from django.db import models
from users.models import CustomUser

class FCMDevice(BaseFCMDevice):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="fcm_devices")
