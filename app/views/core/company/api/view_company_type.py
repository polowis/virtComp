from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import BuildingType


class CompanyTypeView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            data = list(BuildingType.objects.values())
            return JsonResponse(data, safe=False)
        data = {"request": "419"}
        return JsonResponse(data)