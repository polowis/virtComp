from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import Company
from app.core.mixin.base import UserLoggedInRequiredMixinJSON


class CompanyView(View, UserLoggedInRequiredMixinJSON):
    """
    URL: /api/v1/company/

    SUPPORT_METHOD: ['GET', 'POST']

    HELP: GET method: Retrieve company information. POST method: Create company

    PERMISSION: GET: Company logged in, POST: user logged in

    RETURN: JSON response
    """
    def get(self, request: HttpRequest):
        """
        Return the company information
        """
        return JsonResponse(request.company.to_dict())
    
    def post(self, request: HttpRequest):
        """
        Create a new company
        """
        if request.user.is_authenticated:
            company_name = request.POST.get('companyName', None)
            continent = request.POST.get('continent', None)
            if company_name is None:
                data = {'error': True, 'message': 'missing company name'}
                return JsonResponse(data)
            if Company.objects.can_create_company(company_name, continent):
                try:
                    Company.objects.create_company(company_name, request.user, continent)
                    data = {'error': False, 'message': 'sucessfully created', 'redirect_url': '/home/'}
                    return JsonResponse(data)
                except Exception:
                    data = {'error': True, 'message': 'Unable to create company'}
                    return JsonResponse(data)
            data = {'error': True, 'message': 'Unable to create company'}
            return JsonResponse(data)