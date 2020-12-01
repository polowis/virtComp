from django.contrib.auth import authenticate
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from app.core.validator.base import Validator


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



class UserAvailability(View):
    def post(self, request: HttpRequest):
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)

        if username is not None and email is not None:
            if self.has_exists_email() or self.has_exists_username():
                data = {'available': 'false'}
                return JsonResponse(data)
            data = {'available': 'true'}
            return JsonResponse(data)
        data = {'available': 'false'}
        return JsonResponse(data)
    
    def username_exists(self, username, email):
        return User.objects.filter(username=username).exists() 
    
    def email_exists(self, email):
        return User.objects.filter(email=email).exists()
    

    def has_exists_email(self, email):
        if Validator.is_email(email):
            if self.email_exists(email):
                return True
        return False
    
    def has_exists_username(self, username):
        if Validator.is_alphanumeric(username):
            if self.username_exists(username):
                return True
        return False