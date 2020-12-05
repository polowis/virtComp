
from django.db import models
from django.contrib.auth.models import User
from app.models.company.company import Company
import random, time, math


current_time = lambda: int(round(time.time() * 1000))
def generate_unique_id():
    """generate unique id"""
    character = "1234567890abcdefghjiklmnopqrstuvwxyzABCDEFGHJIKLMNOPQRSTUVWSTUVWXYZ"
    temp_id = ""
    for i in range(32):
        temp_id += character[(math.floor(random.random() * len(character)))]
        
    return temp_id + str(current_time())


class Corporation(models.Model):
    corporation_id = models.CharField(max_length=255, default=generate_unique_id)
    corporation_type = models.CharField(max_length=255)
    corporation_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False)
    level = models.IntegerField(default=0)
    storage = models.IntegerField(default=0)
    max_storage = models.IntegerField(default=0)
    status = models.CharField(max_length=255)
    employees = models.IntegerField(default=0)
    max_employees = models.IntegerField(default=0)
    current_rent_cost = models.DecimalField(max_digits=20, decimal_places=4, default=0)

