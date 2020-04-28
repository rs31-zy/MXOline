from django.contrib import admin
from django.apps import AppConfig

# Register your models here.
from apps.users.models import UserProfile
from django.contrib.auth.admin import UserAdmin
class UserProfileAdmin(admin.ModelAdmin):
    pass
class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = '用户'

admin.site.register(UserProfile, UserAdmin)