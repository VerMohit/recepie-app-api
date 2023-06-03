"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# If we change language of django and want to do it everywhere, it can be done in configurations, anywhere _ is used
# - BEST PRACTICE
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define admin pages for users"""

    # These fields were used to check test_users_list under test_admin.py
    # order the users by id
    ordering = ['id']
    # display user email and name in the list display
    list_display = ['email', 'name']

    # These fields were tested against the test_edit_user_page
    fieldsets = (
        ('INSERT TITLE FOR HEADING HERE!!', {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']

    # These fields were tested against the test_create_user_page
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),  # assigns custom CSS classes in the admin
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


# Register custom user model. Specify UserAdmin to use custom admin
admin.site.register(models.User, UserAdmin)
