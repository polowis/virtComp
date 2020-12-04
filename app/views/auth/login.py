from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from setting import settings
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_IF_LOGGED_IN)
        return render(request, self.template_name)
    
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_IF_LOGGED_IN)
            
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            pass

class LogoutView(View):
    def post(self, request: HttpRequest):
        logout(request)
        data  = {'message': 'success', 'redirect_url': '/'}
        return JsonResponse(data)
