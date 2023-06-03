"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserAdmin(BaseUserAdmin):
    """Define admin pages for users"""

    # order the users by id
    ordering = ['id']
    # display user email and name in the list display
    list_display = ['email', 'name']


# Register custom user model. Specify UserAdmin to use custom admin
admin.site.register(models.User, UserAdmin)
