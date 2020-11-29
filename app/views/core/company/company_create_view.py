from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from app.models.company import Company

class CompanyCreateView(View):
    
    template_name = 'core/company/create.html'

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return HttpResponse(status=419)
    
    def post(self, request: HttpRequest):
        pass


class CompanyAvailability(View):
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
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
        return Company.objects.get(name__iexact=name) is not None

