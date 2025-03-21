from django.db import models
from django.contrib.auth.models import User, AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(blank=True, null=True)
    profile_img = models.ImageField(blank=True, null=True)