from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Travel)
admin.site.register(models.Country)
admin.site.register(models.State)
admin.site.register(models.City)
admin.site.register(models.Area)