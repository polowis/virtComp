from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from app.models.company import Company
from app.core.validator.base import Validator

class CompanyCreateView(View):
    
    template_name = 'core/company/create.html'

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return HttpResponse(status=419)
    
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            company_name = request.POST.get('companyName', None)
            if company_name is None:
                data = {'message': 'missing company name'}
            if Validator.is_alphanumeric(company_name):
                try:
                    company = Company.objects.create_company(company_name, request.user.username, request.user)
                    company.save()
                    data = {'message': 'Company successfully created'}
                    return JsonResponse(data)

                except:
                    data = {'message': 'An error occurred'}
                    return JsonResponse(data)

            data = {'message': 'Invalid company name'}
            return JsonResponse(data)
        return HttpResponse(status=419)

class CompanyAvailability(View):
    def post(self, request: HttpRequest):
        company_name = request.POST.get('companyName', None)
        if request.user.is_authenticated and Validator.is_alphanumeric(company_name):
            if self.company_is_available(request.POST.get('companyName', None)):
                data = {
                    "available": True
                }
                return JsonResponse(data)

            data = {
                "available": False
            }

            return JsonResponse(data)
        return HttpResponse(status=419)
    
    def company_is_available(self, name):
        if name is None:
            return False
        return Company.objects.filter(company_name=name.lower()).first() is None

