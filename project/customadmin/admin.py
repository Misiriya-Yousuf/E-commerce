from django.contrib import admin
from .models import UserProfile,Product

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blocked')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Product)
