from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from app.models.core import Company
from app.core.validator.base import Validator


class CompanyCreateView(View):
    
    template_name = 'core/company/create.html'

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return HttpResponse(status=419)
    
    def post(self, request: HttpRequest):
        company_manager = CompanyAvailability()
        if request.user.is_authenticated:
            company_name = request.POST.get('companyName', None)
            continent = request.POST.get('continent', 'asia')
            if company_name is None:
                data = {'message': 'missing company name'}
            if company_manager.can_create_company(company_name):
                try:
                    company = Company.objects.create_company(company_name, request.user, continent)
                    company.balance = 300
                    company.save()
                    data = {'error': False, 'redirect_url': '/home/'}
                    return JsonResponse(data)

                except Exception as e:
                    print(e)
                    data = {'error': True, 'message': 'An error occurred'}
                    return JsonResponse(data)

            data = {'error': True, 'message': 'Invalid company name'}
            return JsonResponse(data)
        return HttpResponse(status=419)


class CompanyAvailability(View):
    def post(self, request: HttpRequest):
        company_name = request.POST.get('companyName', None)
        if request.user.is_authenticated and self.has_valid_company_name(company_name):
            if self.company_is_available(request.POST.get('companyName', None)):
                data = {
                    "available": True
                }
                return JsonResponse(data)

            data = {
                "available": False
            }

            return JsonResponse(data)

        data = {
            "available": False,
            "error": "Unknown error"
        }
        return JsonResponse(data)
    
    def has_valid_company_name(self, company_name):
        return Validator.is_alphanumeric(company_name) and Validator.has_below(company_name, 20)
    
    def company_is_available(self, name):
        if name is None:
            return False
        return Company.objects.filter(company_name=name.lower()).first() is None
        # return true if no matching found
    
    def can_create_company(self, company_name):
        return self.company_is_available(company_name) and self.has_valid_company_name(company_name)

