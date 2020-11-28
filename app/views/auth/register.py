from django.contrib.auth import authenticate
from django.views import View
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterView(View):
    template_name = "auth/register.html"
    
    def get(self, request: HttpRequest):
        return render(request, self.template_name)
    
    def post(self, request: HttpRequest):
        post_username = request.POST.get('username', None)
        post_email = request.POST.get('email', None)
        post_password = request.POST.get('password', None)

        if self.user_exists(post_username, post_email):
            msg = 'User already exists'
        else:
            user = User.objects.create_user(post_username, post_email, post_password)
            login(request, user)

            return redirect('/home')

        

    def user_exists(self, username, email):
        return User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()