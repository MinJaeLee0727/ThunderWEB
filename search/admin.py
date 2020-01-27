from django.contrib import admin
from .models import matches, users

# Register your models here.

admin.site.register(users)
admin.site.register(matches)
