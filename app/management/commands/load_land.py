from django.core.management.base import BaseCommand, CommandError
from app.models.constants.land import Land
    

class Command(BaseCommand):
    help = 'Load a CSV file to database'

    default_path = './csv_data/landData.csv'
    
    def handle(self, *args, **options):
        try:
            Land.objects.load_land(self.default_path)
            print('successfully loaded land')
        except Exception as e:
            raise CommandError(e)