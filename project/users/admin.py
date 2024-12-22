# admin.py
from django.contrib import admin
from .models import OtpToken

@admin.register(OtpToken)
class OtpTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'otp_created_at', 'otp_expires_at')
    search_fields = ('user__username', 'user__email')
