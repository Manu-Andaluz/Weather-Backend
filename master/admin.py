from django.contrib import admin
from .models import Secrets, Entries
# Register your models here.

admin.site.register(Secrets)
admin.site.register(Entries)
