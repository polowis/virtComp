from django.core.management.base import BaseCommand, CommandError
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
        try:
            Landscape.objects.create_multiple_landscape(continent, number_of_lands)
        except Exception as e:
            raise CommandError(e)
        