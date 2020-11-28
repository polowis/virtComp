from django.http import HttpResponse
from django.http import HttpRequest
from django.template import loader
from virtComp.models.material import Material

class ProductView():
    def get_material_list(self):
        pass

    def create_material(self, request: HttpRequest):
        material = Material()
        material.name = request.POST['name']
        material.save()