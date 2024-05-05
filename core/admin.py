# core/admin.py
from django.contrib import admin
from .models import UserProfile, SiteSettings

admin.site.register(UserProfile)
admin.site.register(SiteSettings)
