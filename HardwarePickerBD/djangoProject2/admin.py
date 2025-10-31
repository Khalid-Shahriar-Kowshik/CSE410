import re
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin, GroupAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


class MyAdminSite(AdminSite):
    site_header = _("HardwarePickerBD")
    site_title = _("Site Admin")
    index_title = _("Dashboard")

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        app_list = [app for app in app_list if app['app_label'] != 'contenttypes']

        for app in app_list:
            if app['app_label'] == 'auth':
                app['models'] = [m for m in app['models'] if m['object_name'] != 'Permission']

        for app in app_list:
            if app['app_label'] == 'guides':
                filtered = []
                for m in app['models']:
                    if m['object_name'].lower() == 'guidesimagess':
                        continue
                    if m.get('name', '').lower() == 'guides imagess':
                        m['name'] = 'View Guides'
                    filtered.append(m)
                app['models'] = filtered

        to_move_names = {'CartItem', 'Order', 'OrderItem', 'UserProfile'}
        moved = []
        for app in app_list:
            remaining = []
            for m in app['models']:
                if m['object_name'] in to_move_names:
                    moved.append(m)
                else:
                    remaining.append(m)
            app['models'] = remaining

        app_list = [app for app in app_list if app['models']]

        if app_label is None and moved:
            app_list.append({
                'name': 'Profiles and Orders',
                'app_label': 'userprofile',
                'models': moved
            })

        return app_list


my_admin = MyAdminSite(name='myadmin')

try:
    my_admin.unregister(ContentType)
    my_admin.unregister(Permission)
except Exception:
    pass

for model, admin_class in [(User, CustomUserAdmin), (Group, GroupAdmin)]:
    try:
        my_admin.unregister(model)
    except admin.sites.NotRegistered:
        pass
    my_admin.register(model, admin_class)


for model in apps.get_models():
    if model in (User, Group, ContentType, Permission):
        continue
    try:
        my_admin.register(model)
    except admin.sites.AlreadyRegistered:
        pass