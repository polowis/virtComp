from django.core.management.base import BaseCommand, CommandError
import csv
from app.models.constants.company_category import CompanyCategory


class Command(BaseCommand):
    help = 'Load a CSV file to database'

    default_path = './csv_data/companytype.csv'
    
    def handle(self, *args, **options):
        try:
            with open(self.default_path) as f:
                reader = csv.reader(f)
                for row in reader:
                    default_value = {
                        'building_cost': row[1],
                        'building_rent': row[2],
                        'upgrade_cost': row[3],
                        'upgrade_cost_growth': row[4],
                        'max_employees': row[5],
                        'max_employees_growth': row[6],
                        'max_storage': row[7],
                        'max_storage_growth': row[8],
                        'can_sell': self.convert_bool_value(row[9])
                    }
                    obj, created = CompanyCategory.objects.update_or_create(category=row[0],
                                                                            defaults=default_value)

                    print('Load data complete')
        except Exception as e:
            raise CommandError(e)
    
    def convert_bool_value(self, value):
        if value.lower() in ['true','1', 'yes',]:
            return True
        
        if value.lower() in ['false', '0', 'no']:
            return False
        