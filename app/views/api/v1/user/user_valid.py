from django.views import View
from django.http import HttpRequest, JsonResponse
from app.models import User


class UserValid(View):
    """
    URL: /api/v1/user/valid/

    SUPPORT_METHOD: ['POST']

    HELP: Check if user provided valid credential before creating new account

    PERMISSION: None

    RETURN: JSON response
    """
    def post(self, request: HttpRequest):
        post_username = request.POST.get('username', None)
        post_email = request.POST.get('email', None)
        if User.objects.can_create_account(post_username, post_email):
            data = {'error': False, 'message': "You can create an account"}
            return JsonResponse(data)
        data = {'error': True, 'message': "You need to provided a valid username and email address"}
        return JsonResponse(data)