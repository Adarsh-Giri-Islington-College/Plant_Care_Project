from django.contrib import admin
from django.urls import path
from order import views

urlpatterns = [
    path('', views.payment, name='payment'),
    path('khalti_payment', views.khalti_payment, name='khalti_payment'),
    path('verify_payment', views.verify_payment, name='verify_payment'),
    path('COD', views.COD, name='COD'),
    path('order_history', views.order_history, name='order_history'),
    path('admin_view_orders', views.admin_view_orders, name='admin_view_orders'),
]