from django.contrib.auth import authenticate
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from app.core.validator.base import Validator


class RegisterView(View):
    template_name = "auth/register.html"
    
    def get(self, request: HttpRequest):
        return render(request, self.template_name)
    
    def post(self, request: HttpRequest):
        post_username = request.POST.get('username', None)
        post_email = request.POST.get('email', None)
        post_password = request.POST.get('password', None)
        post_repeat_password = request.POST.get('repeatpassword', None)

        if self.user_exists(post_username, post_email):
            data = {'msg': 'User already exists'}
            return JsonResponse(data)
        
        if not self.has_valid_credential(post_username, post_email):
            data = {'msg': 'Username or email is invalid'}
            return JsonResponse(data)
        
        if self.password_dont_match(post_password, post_repeat_password):
            data = {'msg': 'Password does not match'}
            return JsonResponse(data)
        
        user = User.objects.create_user(post_username, post_email, post_password)
        login(request, user)

        return redirect('/home/')

    def user_exists(self, username, email):
        return User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()
    
    def has_valid_credential(self, username, email):
        return Validator.is_alphanumeric(username) and Validator.is_email(email)
    
    def password_dont_match(self, password, repeatpassword):
        if password is not None and repeatpassword is not None:
            return password != repeatpassword
        return False



class UserAvailability(View):
    def post(self, request: HttpRequest):
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)

        if username is not None and email is not None:
            if self.has_exists_email(email) or self.has_exists_username(username):
                data = {'available': False}
                return JsonResponse(data)

            if self.has_valid_email(email) and self.has_valid_username(username):
                data = {'available': True}
                return JsonResponse(data)

            data = {'available': False}
            return JsonResponse(data)

        data = {'available': True}
        return JsonResponse(data)
    
    def username_exists(self, username):
        return User.objects.filter(username=username).exists() 
    
    def email_exists(self, email):
        return User.objects.filter(email=email).exists()
    

    def has_exists_email(self, email):
        if self.has_valid_email(email):
            if self.email_exists(email):
                return True
        return False
    
    def has_exists_username(self, username):
        if self.has_valid_username(username):
            if self.username_exists(username):
                return True
        return False
    
    def has_valid_username(self, username):
        return Validator.is_alphanumeric(username)
    
    def has_valid_email(self, email):
        return Validator.is_email(email)