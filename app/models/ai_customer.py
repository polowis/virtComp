from django.db import models


import time, uuid

current_time = lambda: int(round(time.time() * 1000))


def generate_unique_id():
    """generate unique id"""
    return str(uuid.uuid1()).replace("-", "")



class AI_Customer(models.Model):
    customer_id = models.CharField(max_length=255, default=generate_company_id)
    class_level = models.Integer()
    salary = models.DecimalField()
    productivity = models.IntegerField()
    stress = models.IntegerField()
    hour_of_work_per_day = models.IntegerField()
    company = models.CharField(max_length=255)
    created_at = models.DateTimeField(editable=False)
