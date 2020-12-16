from django.core.management.base import BaseCommand
from app.models import Landscape


class Command(BaseCommand):
    help = 'Bulk create land in database'

    def add_arguments(self, parser):
        parser.add_argument('number_of_lands', nargs='+', type=int)
        parser.add_argument('--continent', nargs='?', type=str,
                            default='asia')

    def handle(self, *args, **options):
        number_of_lands = options['number_of_lands']
        continent: str = options['continent']
        for number_of_land in number_of_lands:
            for i in range(int(number_of_land)):
                landscape: Landscape = Landscape.objects.create_land(continent)
                print("Created landscape with id {}".format(landscape.land_id))
