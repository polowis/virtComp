from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models.constants.company_category import CompanyCategory


class CompanyTypeView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            data = list(CompanyCategory.objects.values())
            return JsonResponse(data, safe=False)
        data = {"request": "419"}
        return JsonResponse(data)