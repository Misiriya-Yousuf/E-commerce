from django.shortcuts import render
# Create your views here.

def user_management(request):
     return render(request,'user_manage.html')

def category_management(request):
     return render(request,'category_manage.html')

def product_management(request):
     return render(request,'product_manage.html')
