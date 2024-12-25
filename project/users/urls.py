from django.urls import path
from . import views

urlpatterns = [
path('',views.signin_view,name='signin'),
path('home/',views.home,name='home'),
path('dashboard/',views.admin_dashboard,name = 'dashboard'),
path('signout/',views.signout_view,name='signout'),
path('signup/',views.signup_view,name='signup'),
path('verify/<int:user_id>/', views.verify_view, name='verify'),
path('resend/<int:user_id>/',views.resend_view,name='resend')
]