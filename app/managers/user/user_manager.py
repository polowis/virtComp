from django.db import models
from app.core.validator.base import Validator


class UserManager(models.Manager):
    """
    The user manager class
    """
    def username_exists(self, username: str) -> bool:
        """Return true if username exists"""
        return self.filter(username=username).exists()
    
    def email_exists(self, email: str) -> bool:
        """return true if email exists"""
        return self.objects.filter(email=email).exists()
    
    def can_create_account(self, username: str, email: str) -> bool:
        """
        Return true if user can create an account
        This will make sure that both email and username are not duplicated
        """
        email_valid = not self.email_exists(email) and Validator.is_email(email)
        username_valid = not self.username_exists(username) and Validator.is_alphanumeric(username)
        return email_valid and username_valid