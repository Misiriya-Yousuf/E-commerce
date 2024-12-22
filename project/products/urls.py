from django.urls import path
from . import views

urlpatterns = [
path('list/',views.products,name='products'),
path('details/',views.products_details,name='products_details')
]