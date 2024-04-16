from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('view_users/', views.view_users, name='view_users'),
    path('edit_user_details/<int:user_id>', views.edit_user_details, name='edit_user_details'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('ban_user/<int:user_id>', views.ban_user, name='ban_user'),
    path('unban_user/<int:user_id>', views.unban_user, name='unban_user'),
    path('user_search/', views.user_search, name='user_search'),
]
