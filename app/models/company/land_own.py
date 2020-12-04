from django.db import models
import time, math


current_time = lambda: int(round(time.time() * 1000))

def generate_unique_id():
    """generate unique id"""
    character = "1234567890abcdefghjiklmnopqrstuvwxyzABCDEFGHJIKLMNOPQRSTUVWSTUVWXYZ"
    temp_id = ""
    for i in range(32):
        temp_id += str(math.floor(random.random() * len(character)))
        
    return temp_id + str(current_time())


class LandOwn(models.Model):
    land_id = models.CharField(max_length=255, default=generate_unique_id)
    level = models.IntegerField(default=0)
    company_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
