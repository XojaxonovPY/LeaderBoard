from django.contrib import admin

from auth_apps.models import User
from .models import UploadedFile

admin.site.register(UploadedFile)

@admin.register(User)
class ModelNameAdmin(admin.ModelAdmin):
    pass

