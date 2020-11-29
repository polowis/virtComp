from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

class CompanyCreateView(View):
    
    template_name = 'core/company/create.html'

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return HttpResponse(status=419)
    
    def post(self, request: HttpRequest):
        pass

