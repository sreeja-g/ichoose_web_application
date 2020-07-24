from djongo import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=16)
    address = models.TextField()
    verification_status=models.BooleanField(default=False)
    verification_applied = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, unique=True)
    def __str__(self):

        return self.username
