from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as AuthUser
from .models import User, Organisation


admin.site.register(User)
admin.site.register(Organisation)
