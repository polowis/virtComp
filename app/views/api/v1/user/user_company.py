from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import Company
from app.core.mixin.base import UserLoggedInRequiredMixinJSON


class UserCompany(View, UserLoggedInRequiredMixinJSON):
    """
    URL: /api/v1/user/company/

    SUPPORT_METHOD: ['GET']

    HELP: Retrieve all company belongs to current user

    RETURN: JSON response
    """
    def get(self, request: HttpRequest):
        company = list(Company.objects.filter(owner_name=request.user.username).values())
        return JsonResponse(company, safe=False)