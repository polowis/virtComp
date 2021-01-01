from django.core.management.base import BaseCommand, CommandError
from app.models.constants import Place


class Command(BaseCommand):
    help = 'Load a CSV file to database'

    default_path = './csv_data/place.csv'
    
    def handle(self, *args, **options):
        try:
            Place.objects.load_data(self.default_path)
            print('Successfully loaded place')
        except Exception as e:
            raise CommandError(e)