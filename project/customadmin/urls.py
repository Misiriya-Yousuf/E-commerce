from django.urls import path
from . import views

urlpatterns = [
    path('manage-users/', views.manage_users, name='user_management'),
    path('block-user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock-user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('category_management/',views.category_management,name = 'category_management'),
    path('list-product/',views.list_product,name = 'list_product'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/update-stock/', views.update_stock, name='update_stock')
]

