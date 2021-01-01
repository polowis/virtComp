from django.core.management.base import BaseCommand, CommandError
import os
    

class Command(BaseCommand):
    help = 'Load all data from csv file to database'

    
    def handle(self, *args, **options):
        try:
            os.system('./manage.py load_land')
            os.system('./manage.py load_building')
            os.system('./manage.py load_place')
        except Exception as e:
            raise CommandError(e)