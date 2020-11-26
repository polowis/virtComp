from django.contrib.auth.models import AbstractUser
from django.db import models
import time

current_time = lambda: int(round(time.time() * 1000))

def generate_company_id():
    """generate company id"""
    character = "1234567890abcdefghjiklmnopqrstuvwxyzABCDEFGHJIKLMNOPQRSTUVWSTUVWXYZ"
    temp_id = ""
    for i in range(32):
        temp_id += math.floor(random.random() * len(character))
        
    return temp_id + str(current_time())

class User(AbstractUser):
    age = models.IntegerField()
    user_id = models.CharField(max_length=255, default=generate_company_id)
