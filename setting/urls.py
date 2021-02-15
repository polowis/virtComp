"""virtComp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views.exceptions import *
from app.views import *
from django.views.generic import TemplateView
from django.http import HttpRequest
from django.shortcuts import render
from .api_urls import api_pattern


def NewUIView(request: HttpRequest):
    return render(request, 'design_v2/demo.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('home/', HomeView.as_view()),
    path('user/current/', UserView.as_view()),
    path('company/', CompanyView.as_view()),
    path('company/create/', CompanyCreateView.as_view()),
    path('company/hasavailablename/', CompanyAvailability.as_view()),
    path('company/signed/', CompanyLoggedInView.as_view()),
    path('company/current/', CompanyGetView.as_view()),
    path('company/land/all/', LandCompanyView.as_view()),
    path('user/isavailable/', UserAvailability.as_view()),
    path('user/companies/', CurrentUserCompany.as_view()),
    path('api/data/companytype/', CompanyTypeView.as_view()),
    path('land/', LandAvailable.as_view()),
    path('land/<land_id>/view/', LandView.as_view()),
    path('land/<land_id>/buy/', LandBuy.as_view()),
    path('land/<land_id>/rent/', LandRent.as_view()),
    path('design/', NewUIView),
    

] + api_pattern

handler403 = 'app.views.exceptions.base.Error403'
handler404 = 'app.views.exceptions.base.Error404'
handler500 = 'app.views.exceptions.base.Error500'