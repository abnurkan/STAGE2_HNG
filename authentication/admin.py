from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as AuthUser
from .models import User, Organisation

# class UserAdmin(BaseUserAdmin):
#     model = User
#     list_display = ('userId', 'first_name', 'last_name', 'email', 'phone')
#     search_fields = ('first_name', 'last_name', 'email')
#     readonly_fields = ('userId',)
#     ordering = ('email',)

#     fieldsets = (
#         (None, {'fields': ('userId', 'email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
#         #('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         #('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )

# class OrganisationAdmin(admin.ModelAdmin):
#     model = Organisation
#     list_display = ('orgId', 'name', 'description')
#     search_fields = ('name',)
#     readonly_fields = ('orgId',)

# admin.site.register(User, UserAdmin)
# admin.site.register(Organisation, OrganisationAdmin)

admin.site.register(User)
admin.site.register(Organisation)
