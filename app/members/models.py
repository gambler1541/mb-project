from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_img = models.ImageField(upload_to='user')
