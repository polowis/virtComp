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
from app.views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('home/', HomeView.as_view()),
    path('currentuser/', UserView.as_view()),
    path('company/create/', CompanyCreateView.as_view()),
    path('company/hasavailablename/', CompanyAvailability.as_view()),
    path('user/isavailable/', UserAvailability.as_view()),
    path('api/data/companytype/', CompanyTypeView.as_view()),
    path('user/companies/', CurrentUserCompany.as_view()),
    path('logout/', LogoutView.as_view()),
    path('company/corporation/', CompanyView.as_view()),

]
