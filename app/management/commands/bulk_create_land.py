from django.core.management.base import BaseCommand, CommandError
from 

class Command(BaseCommand):
    help = 'Bulk create land in database'

    def add_arguments(self, parser):
        parser.add_argument('number_of_lands', nargs='+', type=int)

    def handle(self, *args, **options):
        number_of_lands = options['number_of_lands']
        for i in range(int(number_of_lands)):
