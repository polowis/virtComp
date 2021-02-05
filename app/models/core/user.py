from django.contrib.auth.models import AbstractUser
from app.managers.user import UserManager


class User(AbstractUser):
    """
    The user based class. Inherit from Django user model
    """
    objects = UserManager()