from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User) # Necessary

# Register your models here.
class UserProfileInline(admin.TabularInline):
    model = UserProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)