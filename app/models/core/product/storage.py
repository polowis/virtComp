from django.db import models
from app.models.core.building import Building
from django.utils import timezone


class StorageManager(models.Manager):
    def create_storage(self, building, max_capacity):
        """Create the storage associated with the given building"""
        return self.create(building=building, max_capacity=max_capacity)


class Storage(models.Model):
    """
    The storage model for handling storage
    """
    building = models.OneToOneField(Building, on_delete=models.CASCADE)
    max_capacity = models.IntegerField()
    current_capacity = models.IntegerField(default=0)
    updated_at = models.DateTimeField()

    objects = StorageManager()

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def put(self, item):
        pass

