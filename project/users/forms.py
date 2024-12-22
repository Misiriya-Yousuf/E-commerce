from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}))

    class Meta:
        model = get_user_model()
        fields = ['username','email','password1','password2']

class OtpVerificationForm(forms.Form):
    otp_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'}))
    
class ResendOtpForm(forms.Form):
    resend_email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your registered email'}))
    
