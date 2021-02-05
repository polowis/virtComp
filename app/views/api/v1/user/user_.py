from django.views import View
from django.http import HttpRequest, JsonResponse
from app.core.mixin.base import UserLoggedInRequiredMixinJSON


class UserView(View, UserLoggedInRequiredMixinJSON):
    """
    URL: /api/v1/user/

    SUPPORT_METHOD: ['GET']

    HELP: Retrieve user information

    RETURN: JSON response
    """
    def get(self, request: HttpRequest):
        user = {
            "id": request.user.id,
            "email": request.user.email,
            "username": request.user.username
        }
        return JsonResponse(user)