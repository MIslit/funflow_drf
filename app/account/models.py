
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/", null=True, blank=True, editable=True)
    email = models.EmailField(max_length=254, unique=True, editable=True)
    about_me = models.TextField(max_length=500, blank=True, editable=True)

    def __str__(self):
        return self.username
