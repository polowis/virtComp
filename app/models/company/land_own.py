from django.db import models
import time, math

from app.models.company import Company

current_time = lambda: int(round(time.time() * 1000))

def generate_unique_id():
    """generate unique id"""
    character = "1234567890abcdefghjiklmnopqrstuvwxyzABCDEFGHJIKLMNOPQRSTUVWSTUVWXYZ"
    temp_id = ""
    for i in range(32):
        temp_id += str(math.floor(random.random() * len(character)))
        
    return temp_id + str(current_time())

class LandOwnManager(models.Manager):
    def create_land(self, level, buy_cost):
        land = self.create(level=level, buy_cost=buy_cost)
        return land

class LandOwn(models.Model):
    land_id = models.CharField(max_length=255, default=generate_unique_id)
    level = models.IntegerField(default=0)
    company_name = models.CharField(max_length=255, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=255, default='')
    buy_cost = models.DecimalField(max_digits=20, decimal_places=4)

    objects = LandOwnManager()
