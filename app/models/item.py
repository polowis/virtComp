from django.db import models




class Item(models.Model):
    name = models.CharField(max_length=255)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=4)
    time_to_produce = models.IntegerField()
    require_factory = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

    class Meta:
        app_label = "app"

