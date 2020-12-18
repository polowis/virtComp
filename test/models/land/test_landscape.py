from django.test import TestCase
from app.models import Landscape, Land


class LandscapeTestCase(TestCase):
    def setUp(self):
        Land.objects.load_land('csv_data/landData.csv')
        self.land: Landscape = Landscape.objects.create_land('asia')
    
    def test_land_is_created(self):
        self.assertEquals(self.land.continent, 'asia')