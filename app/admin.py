from django.contrib import admin

# Register your models here.
from app.models import Company, Landscape, Land, User

admin.site.register(Company)
admin.site.register(Landscape)
admin.site.register(Land)
admin.site.register(User)