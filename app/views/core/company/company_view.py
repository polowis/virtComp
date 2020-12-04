from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from app.core.util.company import get_current_register_company

class CompanyView(View):
    def get(self, request: HttpRequest):
        template_name = 'company/view.html'
        if request.user.is_authenticated:
            return render(request, template_name)
        return HttpResponse(status=419)
    
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            company = get_current_register_company(request)
            if company is not None:
                company = list(company.values())
                return JsonResponse(data, safe=False)
        return HttpResponse(status=419)
