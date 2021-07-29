from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'display_name', 'email', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('display_name',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('display_name',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)