from django.contrib import admin

# Register your models here.
from .models import Company, Landscape, Land


admin.site.register(Company)
admin.site.register(Landscape)
admin.site.register(Land)