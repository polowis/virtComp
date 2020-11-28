from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect

class UserView(View):
    def get(self, request: HttpRequest):
        next = request.POST.get('next', '/') # get the "next" field from the form, it holds the value of current path
        if request.user.is_authenticated:
            user = {
                "id": request.user.id
                "email": request.user.email,
                "username": request.user.username
            }
            return JsonResponse(user)
        return HttpResponseRedirect(next)