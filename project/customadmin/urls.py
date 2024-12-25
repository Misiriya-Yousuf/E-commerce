from django.urls import path
from . import views

urlpatterns = [
path('user_management/',views.user_management,name = 'user_management'),
path('category_management/',views.category_management,name = 'category_management'),
path('product_management/',views.product_management,name = 'product_management')
]