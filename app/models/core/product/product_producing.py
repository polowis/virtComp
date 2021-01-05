from django.db import models


class ProductProducing(models.Model):
    name = models.CharField(max_length=255)
    expected_quality = models.DecimalField(max_digits=10, decimal_places=2)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()