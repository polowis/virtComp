from django.contrib.auth import authenticate
from django.views import View
from django.http import HttpRequest
from django.shortcuts import render

class RegisterView(View):
    template_name = "auth/register.html"
    
    def get(self, request: HttpRequest):
        return render(request, self.template_name)