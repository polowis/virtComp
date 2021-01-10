from django.db import models
from app.models.core.building import Building


class Storage(models.Model):
    building = models.OneToOneField(Building, on_delete=models.CASCADE)

    