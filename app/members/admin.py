from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',

            ),
        }),
        ('개인정보', {
            'fields': (
                'img_profile',

            ),
        }),
    )


admin.site.register(User, UserAdmin)
