from django.contrib import admin
from django.urls import path
from products import views

urlpatterns = [
    path('', views.display_products, name='display_products'),
    path('product/<int:pk>', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<int:pk>', views.update_product, name='update_product'),
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),
    path('search/', views.search, name='search'),
]