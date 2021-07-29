from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=64)

    def __str__(self):
        if self.display_name != '':
            return self.display_name
        return self.username