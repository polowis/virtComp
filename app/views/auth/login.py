from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpRequest


class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request: HttpRequest):
        return render(request, self.template_name)
    
    def post(self, request: HttpRequest):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            redirect('/')
        else:
            pass
