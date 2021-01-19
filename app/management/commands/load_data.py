from django.core.management.base import BaseCommand, CommandError
import os
import concurrent.futures
import time


class Command(BaseCommand):
    help = 'Load all data from csv file to database'

    command_list = ['load_land', 'load_building', 'load_place', 'load_item']

    def handle(self, *args, **options):
        start = time.time()
        try:
            self.load_data(self.command_list)
            end = time.time()
            print(f"Loaded completed in: {round(end-start, 4)}s")
        except Exception as e:
            raise CommandError(e)

    def load_command(self, command):
        os.system(f'./manage.py {command}')

    def load_data(self, commands):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.load_command, commands)
    
    
