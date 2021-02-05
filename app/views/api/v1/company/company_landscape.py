from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import Landscape


class CompanyLandscape(View):
    def get(self, request: HttpRequest):
        landscapes = list(Landscape.objects.filter(owner_name=request.user.username).values())
        return JsonResponse(landscapes)