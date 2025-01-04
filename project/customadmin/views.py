from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import UserProfile 
from .models import Product,Category
from .forms import CategoryForm,ProductForm                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
from .models import ProductVariant,ProductImage

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
    categories = Category.objects.all()

    if request.method == 'POST':
        # Process product details
        category = Category.objects.get(id=request.POST.get('category'))
        name = request.POST.get('name')
        sale_price = request.POST.get('sale_price')
        discount_price = request.POST.get('discount_price', None)
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        main_image_file = request.FILES.get('main_image')

        # Create main image and product
        main_image = ProductImage.objects.create(image=main_image_file, is_variant=False)
        product = Product.objects.create(
            category=category,
            name=name,
            sale_price=sale_price,
            discount_price=discount_price,
            quantity=quantity,
            description=description,
            main_image=main_image,
        )

        # Process variant images
        variant_images_files = request.FILES.getlist('variant_images_upload')
        if variant_images_files:
            product_variant = ProductVariant.objects.create(product=product)  # Pass the product instance here
            for image_file in variant_images_files:
                variant_image = ProductImage.objects.create(image=image_file, is_variant=True)
                product_variant.variant_images.add(variant_image)

            product_variant.save()

        messages.success(request, f'Product "{product.name}" was added successfully!')
        return redirect('list_product')

    return render(request, 'add_product.html', {'categories': categories})

@login_required
def view_product(request, product_id):
    # Get the product object
    product = get_object_or_404(Product, id=product_id)
    
    # Get all the variants of this product, filter by product to ensure only the right variants are returned
    product_variants = ProductVariant.objects.filter(product=product)

    return render(request, 'view_product.html', {
        'product': product,
        'variants': product_variants,
    })

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        # Process product details
        category = Category.objects.get(id=request.POST.get('category'))
        name = request.POST.get('name')
        sale_price = request.POST.get('sale_price')
        discount_price = request.POST.get('discount_price', None)
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        main_image_file = request.FILES.get('main_image')
        
        # Update the main image
        if main_image_file:
            main_image = ProductImage.objects.create(image=main_image_file, is_variant=False)
            product.main_image = main_image
        
        # Update product details
        product.category = category
        product.name = name
        product.sale_price = sale_price
        product.discount_price = discount_price
        product.quantity = quantity
        product.description = description
        
        # Save updated product
        product.save()

        # Process variant images if they are provided
        variant_images_files = request.FILES.getlist('variant_images_upload')
        if variant_images_files:
            # Create or update product variants
            product_variant, created = ProductVariant.objects.get_or_create(product=product)
            for image_file in variant_images_files:
                variant_image = ProductImage.objects.create(image=image_file, is_variant=True)
                product_variant.variant_images.add(variant_image)
            product_variant.save()

        messages.success(request, f'Product "{product.name}" was updated successfully!')
        return redirect('list_product')

    else:
        # If it's a GET request, pre-populate the form with existing product data
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {
        'form': form,
        'categories': categories,
        'product': product
    })

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

# View to handle category management (adding, editing, deleting)
def category_management(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            # Add new category
            Category.objects.create(name=name)
            return redirect('category_management')

    return render(request, 'category_manage.html', {'categories': categories})


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        # Form for editing category
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_management')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'edit_category.html', {'category': category, 'form': form})


# View to delete a category
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_management')

