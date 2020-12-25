from django.db import models


class AI_Customer(models.Model):
    customer_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    qualification = models.DecimalField(max_digits=5, decimal_places=2)
    class_level = models.Integer()
    salary = models.DecimalField(max_digits=5, decimal_places=2)
    productivity = models.DecimalField(max_digits=5, decimal_places=2)
    stress = models.DecimalField(max_digits=5, decimal_places=2)
    hour_of_work_per_day = models.IntegerField()
    company_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(editable=False)
