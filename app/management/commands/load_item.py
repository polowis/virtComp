from django.core.management.base import BaseCommand, CommandError
from app.models.constants import Item


class Command(BaseCommand):
    help = 'Load a CSV file to database'

    default_path = './csv_data/item.csv'
    
    def handle(self, *args, **options):
        try:
            Item.objects.load_items(self.default_path)
            print('successfully loaded items')
        except Exception as e:
            raise CommandError(e)
    