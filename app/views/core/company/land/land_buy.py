from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse

class LandBuy(View):
    def post(self, request: HttpRequest, land_id=None):
        pass