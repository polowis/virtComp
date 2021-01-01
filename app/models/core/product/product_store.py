from django.db import models
from app.core.util.base import generate_unique_id
from app.models.core.building import Building
from app.models.constants import Item
from django.utils import timezone


class ProductStored(models.Model):
    """The products stored in each building"""
    record_id = models.CharField(max_length=255, default=generate_unique_id)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)