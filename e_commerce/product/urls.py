from django.urls import path
from . import views
from django.urls import path
from .views import *
urlpatterns = [
    path('',views.index,name="index"),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('profile/<int:id>/',views.profile_details,name='profile'),
    path('profile/edit/<int:id>/',views.profile_edit,name='profile_edit'),
    path('order/<int:id>/', views.order_details_view, name='order_details'),
    # path('order/invoice/<int:id>/', views.download_invoice, name='download_invoice'),
    path('order/invoice/<int:id>/', views.download_invoice, name='download_invoice'),



    path("products/<int:product_id>/", views.edit_product_api, name="edit_product_api"),
    path('products/delete/<int:product_id>/', views.delete_product_api, name='delete_product_api'),


]
