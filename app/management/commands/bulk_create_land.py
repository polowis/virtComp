from django.core.management.base import BaseCommand, CommandError
from numpy.random import choice
from app.models.company.land_own import LandOwn
from app.models.constants.land import Land
from random import uniform

class Command(BaseCommand):
    help = 'Bulk create land in database'

    def add_arguments(self, parser):
        parser.add_argument('number_of_lands', nargs='+', type=int)

    def get_probability(self):
        return [0.23, 0.15, 0.13, 0.1, 0.09, 0.08, 0.06, 0.06, 0.05, 0.03, 0.02]
    
    def get_land_level(self):
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def handle(self, *args, **options):
        number_of_lands = options['number_of_lands']
        for number_of_land in number_of_lands:
            for i in range(int(number_of_land)):
                land_level = choice(self.get_land_level(), p=self.get_probability())
                land: Land = Land.objects.get(level=land_level)
                land_cost = uniform(float(land.min_land_cost), float(land.max_land_cost))
                land_created = LandOwn.objects.create_land(land_level, land_cost)
                land_created.save()
                print(f'Create land level {land_level} with the price at {land_cost}')


