from django.core.management.base import BaseCommand, CommandError
from app.models.constants.building_type import BuildingType


class Command(BaseCommand):
    help = 'Load a CSV file to database'

    default_path = './csv_data/buildingType.csv'
    
    def handle(self, *args, **options):
        try:
            BuildingType.objects.load_building_type(self.default_path)
        except Exception as e:
            raise CommandError(e)
    

        