from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    pass

class User(AbstractUser):
    profile_img = models.ImageField(upload_to='user')
