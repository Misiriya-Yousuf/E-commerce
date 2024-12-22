from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
import random


class OtpToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True,null=True)
    otp_email = models.EmailField()

    def generate_otp(self):
        """Generate a random 6-digit OTP."""
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_expires_at = timezone.now() + timezone.timedelta(minutes=2)  # OTP expires in 2 minutes
        self.save()
        return self.otp_code


