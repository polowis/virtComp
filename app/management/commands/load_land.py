from django.core.management.base import BaseCommand, CommandError
import csv
from app.models.constants.land import Land

class Command(BaseCommand):
    help = 'Load a CSV file to database'

    default_path = './csv_data/landData.csv'
    
    def handle(self, *args, **options):
        try:
            with open(self.default_path) as f:
                reader = csv.reader(f)
                for row in reader:
                    default_value = {
                        'cost': row[1],
                        'rent': row[2],
                        'max_land_cost': row[3],
                        'min_land_cost': row[4]
                    }
                    obj, created = Land.objects.update_or_create(level=row[0],
                                                                 defaults=default_value)
                    print('Loaded data at', default_value)
        except Exception as e:
            raise CommandError(e)