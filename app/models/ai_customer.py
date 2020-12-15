from django.db import models



class AI_Customer(models.Model):
    customer_id = models.CharField(max_length=255)
    class_level = models.Integer()
    salary = models.DecimalField()
    productivity = models.IntegerField()
    stress = models.IntegerField()
    hour_of_work_per_day = models.IntegerField()
    company = models.CharField(max_length=255)
    created_at = models.DateTimeField(editable=False)
