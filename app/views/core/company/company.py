from django.views import View
from django.http import HttpRequest, JsonResponse
from app.core.util.company import get_current_register_company


class CompanyGetView(View):
    def get(self, request: HttpRequest):
        company = get_current_register_company(request)
        if company is not None:
            data = {'company': company.company_name}
            return JsonResponse(data)
        data = {'company': ''}
        return JsonResponse(data)