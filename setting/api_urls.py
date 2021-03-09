"""
Contains API routes
"""

from django.urls import path, include
from app.views.api.v1.user import UserView, UserCompany, UserCompanySign, UserValid
from app.views.api.v1.company import CompanyView
import app.views.api.v1.landscape as Landscape
import app.views.api.v1.constants as Constants
import app.views.api.v1.building as Building

API_VERSION = 'v1'

user_pattern = [
    path('', UserView.as_view()),
    path('company/', UserCompany.as_view()),
    path('company/sign/', UserCompanySign.as_view()),
    path('valid/', UserValid.as_view()),
]

landscape_pattern = [
    path('', Landscape.LandscapeView.as_view()),
    path('<land_id>/view/', Landscape.LandscapeID.as_view()),
    path('<land_id>/buy/', Landscape.LandscapeBuy.as_view()),
    path('<land_id>/rent/', Landscape.LandscapeRent.as_view()),
    path('browse/', Landscape.LandscapeBrowse.as_view())

]

company_pattern = [
    path('', CompanyView.as_view())
]

constants_pattern = [
    path('buildingtypename/', Constants.BuildingTypeName.as_view())
]

building_pattern = [
    path("create/", Building.BuildingCreate.as_view())
]

api_pattern = [
    path(f'api/{API_VERSION}/user/', include(user_pattern)),
    path(f'api/{API_VERSION}/company/', include(company_pattern)),
    path(f'api/{API_VERSION}/landscape/', include(landscape_pattern)),
    path(f'api/{API_VERSION}/constants/', include(constants_pattern)),
    path(f'api/{API_VERSION}/building/', include(building_pattern))

]