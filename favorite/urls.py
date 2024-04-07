from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_favorite, name='display_favorite'),
    path('add_favorite/<int:pk>', views.add_favorite, name='add_favorite'),
    path('delete_favorite/<int:pk>', views.delete_favorite, name='delete_favorite'),
]