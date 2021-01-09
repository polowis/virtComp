from django.core.management.base import BaseCommand, CommandError
import os
import concurrent.futures
import threading

class Command(BaseCommand):
    help = 'Load all data from csv file to database'

    command_list = ['load_land', 'load_building', 'load_place']

    
    def handle(self, *args, **options):
        try:
            self.load_data(self.command_list)
        except Exception as e:
            raise CommandError(e)

    def load_command(self, command):
        os.system(f'./manage.py {command}')

    def load_data(self, commands):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.load_command, commands)
    
    
