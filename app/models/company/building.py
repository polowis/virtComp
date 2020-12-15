from django.db import models
from app.core.util.base import generate_unique_id
from app.models import Company, Landscape, Building


class BuildingManager(models.Manager):
    def create_building(self, building_type: str, building_name: str,
                        company: Company) -> Building:
        building: Building = self.create(building_type=building_type,
                                         building_name=building_name,
                                         company=company)

        return building


class Building(models.Model):
    building_id = models.CharField(max_length=255, default=generate_unique_id)
    building_type = models.CharField(max_length=255)
    building_name = models.CharField(max_length=255)
    current_level = models.IntegerField()
    company_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    current_storage = models.IntegerField()
    max_storage = models.IntegerField()
    current_employee = models.IntegerField(default=0)
    max_employee = models.IntegerField()
    is_buy = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=False)
    rent_cost = models.DecimalField(max_digits=20, decimal_places=4)
    landscape = models.OneToOneField(Landscape, on_delete=models.CASCADE,
                                     primary_key=True)
    last_collected_money_at = models.DateTimeField()

    objects = BuildingManager()
