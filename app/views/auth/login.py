from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, JsonResponse
from setting import local_settings


class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(local_settings.REDIRECT_IF_LOGGED_IN)
        return render(request, self.template_name)
    
    def post(self, request: HttpRequest):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            data = {'status': 'success', 'redirect_url': '/home/'}
            return JsonResponse(data)
        data = {'status': 'error', 'message': 'Username or email does not exist'}
        return JsonResponse(data)


class LogoutView(View):
    def post(self, request: HttpRequest):
        logout(request)
        data = {'message': 'success', 'redirect_url': '/'}
        return JsonResponse(data)
