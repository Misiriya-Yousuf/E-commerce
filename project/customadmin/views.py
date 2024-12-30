from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import UserProfile  # Assuming you're using the Profile model to track blocked users

# List all users for admin
@never_cache
@login_required
def manage_users(request):
    if not request.user.is_superuser:  # Check if user is an admin
        return redirect('dashboard')
    
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'user_manage.html', context)

# Block user
@never_cache
@login_required
def block_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=user)  # Ensure profile exists
    user_profile.blocked = True
    user_profile.save()  # Save the profile
    
    messages.success(request, f"User {user.username} has been blocked successfully.")
    return redirect('user_management')

# Unblock user
@never_cache
@login_required
def unblock_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    user_profile.blocked = False
    user_profile.save()  # Save the profile
    
    messages.success(request, f"User {user.username} has been unblocked successfully.")
    return redirect('user_management')

def some_view(request):
    url = reverse('dashboard')
    return redirect(url)

def category_management(request):
     return render(request,'category_manage.html')

@login_required
def list_product(request):
    """View to list all non-deleted products."""
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query, is_deleted=False)
    else:
        products = Product.objects.filter(is_deleted=False)
    return render(request, 'list_product.html', {'products': products})

@login_required
def delete_product(request, product_id):
    """Soft delete a product."""
    product = get_object_or_404(Product, id=product_id)
    product.is_deleted = True
    product.save()
    messages.success(request, f'Product "{product.name}" was successfully deleted.')
    return redirect('list_product')

@login_required
def add_product(request):
    """View to add a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('list_product')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('list_product')  # Redirect back to the product list
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def update_stock(request, product_id):
    """View to update stock status of a product."""
    product = get_object_or_404(Product, id=product_id, is_deleted=False)
    if product.quantity > 0:
        product.quantity = 0  # Set out of stock
    else:
        product.quantity = 10  # Example: Set to a default value like 10
    product.save()
    messages.success(request, f'Stock status updated for "{product.name}".')
    return redirect('list_product')



