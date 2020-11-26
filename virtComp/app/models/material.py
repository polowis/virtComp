from django.db import models

class Material(models.Model):
    material_to_produce = models.CharField(max_length=255)
    product_from_material = models.CharField(max_length=255)
    quantity = models.IntegerField()

    class Meta:
        app_label = "app"