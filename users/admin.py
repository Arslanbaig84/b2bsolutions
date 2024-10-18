from django.contrib import admin
from .models import CustomUser, UserProfile

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)