from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from app.core.util.company import get_current_register_company


class CompanyView(View):
    def get(self, request: HttpRequest):
        template_name = 'core/corporation/all_view.html'
        if request.user.is_authenticated:
            return render(request, template_name)
        return redirect('/login/')
    
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            company = get_current_register_company(request)
            if company is not None:
                company = list(company.values())
                return JsonResponse(company, safe=False)


class CompanyCorporationView(View):
    def post(self, request: HttpRequest):
        company = get_current_register_company(request)
        if company is not None:
            pass
