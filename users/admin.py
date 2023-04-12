from django.contrib import admin
from .models import Profile
from .models import User

  
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Info', {
                'fields': (
                    'choice',
                    'date',
                ),
            }
        )
    )


admin.site.register(User, CustomUserAdmin)