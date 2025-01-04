from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from . forms import RegisterForm,OtpVerificationForm,ResendOtpForm
from customadmin.models import UserProfile,Product,Category
from . models import OtpToken
from django.contrib.auth import get_user_model

# Create your views here.

@never_cache
def signin_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                # Check if the user is blocked
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.blocked:
                    messages.error(request, "Your account has been blocked. You cannot log in.")
                    return redirect('signin')
            except UserProfile.DoesNotExist:
                # If no profile exists for the user, we just proceed (assuming no blocking logic is set up)
                pass
            
            # If the user is not blocked, proceed with login
            if user.is_superuser:  # Check if the user is an admin (superuser)
                login(request, user)
                return redirect('dashboard')
            else:
                login(request, user)
                messages.success(request, f"Welcome {user.username}, let's get started!!!")
                return redirect('home')
        
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
    
    else:
        return render(request, 'signin.html', {})
    
@never_cache
@login_required
def home(request):
    return render(request,'home.html',{})

@never_cache
@login_required
def admin_dashboard(request):
    products = Product.objects.all()  # Get all products
    if not request.user.is_superuser:  
        return redirect('home')
     # Calculate counts
    user_count = User.objects.count()
    product_count = Product.objects.filter(is_deleted=False).count()
    category_count = Category.objects.filter(is_trashed=False).count()

    return render(request, 'dashboard.html', {
        'user_count': user_count,
        'product_count': product_count,
        'category_count': category_count,
        'products': products})

@never_cache
def signout_view(request):
    logout(request)
    messages.success(request, 'Signed out successfully!')
    return redirect('signin')

@never_cache
def signup_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            otp_token = OtpToken(user=user)
            otp_code = otp_token.generate_otp()  # Generate the OTP and save it

            subject = 'Your OTP verification code'
            message = f"""
                        Hi {user.username},\n
                Your OTP code is {otp_code}. It will expire in 2 minutes.\n
                Please verify the OTP to activate your account!\n
                Best regards,\n
                Team-SignatureSeconds 

                        """
            sender = 'misiriyayousuf369"gmail.com'
            reciever = [user.email]
            # Send OTP to the user's email
            send_mail(
                subject,
                message,
                sender,  
                reciever,
                fail_silently=False,
            )
            messages.success(request, "Account created successfully !!!")
            return redirect('verify',user_id=user.id)  
        
    context = {"form": form}
    return render(request, "signup.html", context)

@never_cache
def verify_view(request, user_id=None):  
    # user_id is passed in the URL or session
    # Fetch user using the user_id passed to the view
    try:
        user = User.objects.get(id=user_id) 
        # Assuming the user_id is passed
    except User.DoesNotExist:
        messages.error(request, "Invalid or expired link!")
        return redirect('signup')

   
    user_otp = OtpToken.objects.filter(user=user).last()
    form = OtpVerificationForm()

    if user_otp:
        otp_expires_at = user_otp.otp_expires_at.isoformat() 
    else:
        otp_expires_at = None 

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')

        # Check if OTP matches
        if user_otp and user_otp.otp_code == otp_code:
            # Check if OTP is still valid (not expired)
            if user_otp.otp_expires_at > timezone.now():
                # Activate the user after successful OTP verification
                user.is_active = True
                user.save()

                messages.success(request, "Account successfully activated! You can log in now.")
                return redirect('signin')  
                # Redirect to a logged-in page or dashboard
            else:
                # OTP expired
                messages.warning(request, "The OTP has expired,request a new one.")
                return redirect('verify', user_id=user_id)  
                # Stay on the OTP verification page
        else:
            # Invalid OTP
            messages.warning(request, "Invalid OTP code. Please try again.")
            return redirect('verify', user_id=user_id)

    context = {"form": form, "user": user, "otp_expires_at": otp_expires_at}
    return render(request, "verify.html", context)

@never_cache
def resend_view(request, user_id=None):
    try:
        
        user = get_user_model().objects.get(id=user_id)  
        # Use get_user_model() to handle custom user models
    except get_user_model().DoesNotExist:
        messages.error(request, "Invalid or expired link!")
        return redirect('signup') 

    # If OTP exists for the user, proceed with resending process
    user_otp = OtpToken.objects.filter(user=user, otp_expires_at__lt=timezone.now()).last()
    if user_otp:
        user_otp.delete()
       


    form = ResendOtpForm()

    if request.method == 'POST':
        form = ResendOtpForm(request.POST)
        if form.is_valid():
            # Get email from the form
            user_email = form.cleaned_data.get('resend_email')

            # Check if the provided email matches the user's email
            if user_email != user.email:
                messages.warning(request, "This email doesn't match the records for this user.")
                return redirect('resend', user_id=user.id)  # Stay on the same page

            # Generate new OTP for the user
            otp_token = OtpToken(user=user)
            otp_code = otp_token.generate_otp()  
            

            subject = 'Your OTP verification code'
            message = f"""
                        Hi {user.username},\n
                Your OTP code is {otp_code}. It will expire in 2 minutes.\n
                Please verify the OTP to activate your account!\n
                Best regards,\n
                Team-SignatureSeconds
                        """
            sender = 'misiriyayousuf369@gmail.com' 
            reciever = [user.email]

            # Send OTP to the user's email
            send_mail(
                subject,
                message,
                sender,
                reciever,
                fail_silently=False,
            )
            messages.success(request, "OTP has been sent successfully!")
            return redirect('verify', user_id=user.id)

        else:
            # If form is invalid, show a warning message
            messages.warning(request, "There was an issue with the form.")
            return redirect('resend', user_id=user.id)  

    context = {"form": form}
    return render(request, "resend.html", context)
