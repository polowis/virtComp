from django.core.management.base import BaseCommand
from app.models import Landscape


class Command(BaseCommand):
    help = 'Bulk create land in database'

    def add_arguments(self, parser):
        parser.add_argument('number_of_lands', nargs='+', type=int)
        parser.add_argument('land_continent', nargs='?', type=str,
                            default='asia')

    def get_probability(self):
        return [0.23, 0.15, 0.13, 0.1, 0.09, 0.08, 0.06, 0.06, 0.05,
                0.03, 0.02]
    
    def get_land_level(self):
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def handle(self, *args, **options):
        number_of_lands = options['number_of_lands']
        continent = options['land_continent']
        for number_of_land in number_of_lands:
            for i in range(int(number_of_land)):
                landscape: Landscape = Landscape.objects.create_land(continent)
                print("Created landscape with id {}".format(landscape.land_id))


