from django.views import View
from django.http import HttpRequest, JsonResponse


class UserView(View):
    def get(self, request: HttpRequest):
       
        if request.user.is_authenticated:
            user = {
                "id": request.user.id,
                "email": request.user.email,
                "username": request.user.username
            }
            return JsonResponse(user)
        user = {
            "id": "none",
        }
        return JsonResponse(user)