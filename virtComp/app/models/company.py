from django.db import models
import math, random
from django.utils import timezone
import time

current_time = lambda: int(round(time.time() * 1000))

BUSINESS_FIELD = ['restaurant', 'real estate', 'market', 'farm']

def generate_company_id():
    """generate company id"""
    character = "1234567890abcdefghjiklmnopqrstuvwxyzABCDEFGHJIKLMNOPQRSTUVWSTUVWXYZ"
    temp_id = ""
    for i in range(32):
        temp_id += str(math.floor(random.random() * len(character)))
        
    return temp_id + str(current_time())

class Company(models.Model):
    company_id = models.CharField(max_length=255, default=generate_company_id)
    company_name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    popularity = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    qualification = models.IntegerField(default=0)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()


    def is_valid_business_type(self, business_type: str):
        return business_type.lower() in BUSINESS_FIELD

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Company, self).save(*args, **kwargs)
    
    class Meta:
        app_label = "app"



    


