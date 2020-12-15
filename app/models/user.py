
from django.db import models
from django.contrib.auth.models import User


class UserPlan(models.Model):
    plan = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=255)
