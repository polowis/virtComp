from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Company)
admin.site.register(Material)
admin.site.register(Item)
admin.site.register(LandOwn)
admin.site.register(Land)