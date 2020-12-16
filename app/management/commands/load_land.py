from django.core.management.base import BaseCommand, CommandError
import csv
from app.models.constants.land import Land


class Row(object):
    """The base row for readability purpose"""
    def __init__(self, row: list):
        self.row = row
    
    @property
    def level(self) -> int:
        return self.row[0]

    @property
    def rent_cost(self) -> float:
        return self.row[2]
    
    @property
    def buy_cost(self) -> float:
        return self.row[1]

    @property
    def max_land_cost(self) -> float:
        return self.row[3]

    @property
    def min_land_cost(self) -> float:
        return self.row[4]
    



class Command(BaseCommand):
    help = 'Load a CSV file to database'

    default_path = './csv_data/landData.csv'
    
    def handle(self, *args, **options):
        try:
            with open(self.default_path) as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    land: Row = Row(row)
                    default_value = {
                        'cost': land.buy_cost,
                        'rent': land.rent_cost,
                        'max_land_cost': land.max_land_cost,
                        'min_land_cost': land.min_land_cost
                    }
                    obj, created = Land.objects.update_or_create(level=land.level,
                                                                 defaults=default_value)
                    print('Loaded data at', default_value)
        except Exception as e:
            raise CommandError(e)