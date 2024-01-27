from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
      fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('my_city',)}),
      )


admin.site.register(CustomUser,CustomUserAdmin)   

    