from django.db import models


import time

current_time = lambda: int(round(time.time() * 1000))


def generate_company_id():
    """generate company id"""
    character = "1234567890abcdefghjiklmnopqrstuvwxyzABCDEFGHJIKLMNOPQRSTUVWSTUVWXYZ"
    temp_id = ""
    for i in range(32):
        temp_id += str(math.floor(random.random() * len(character)))
        
    return temp_id + str(current_time())


class AI_Customer(models.Model):
    customer_id = models.CharField(max_length=255, default=generate_company_id)
    class_level = models.Integer()
    salary = models.DecimalField()
    productivity = models.IntegerField()
    stress = models.IntegerField()
    hour_of_work_per_day = models.IntegerField()
    company = models.CharField(max_length=255)
    created_at = models.DateTimeField(editable=False)
