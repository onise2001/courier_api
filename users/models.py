from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("Admin", "admin"),
        ("Courier", "courier"),
        ("Customer", "customer")
    )
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
