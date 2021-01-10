from django.db import models
from app.models.core.building import Building
from django.utils import timezone


class StorageManager(models.Manager):
    def create_storage(self, building, max_capacity):
        return self.create(building=building, max_capacity=max_capacity)


class Storage(models.Model):
    building = models.OneToOneField(Building, on_delete=models.CASCADE)
    max_capacity = models.IntegerField()
    current_capacity = models.IntegerField(default=0)
    updated_at = models.DateTimeField()

    objects = StorageManager()


    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

