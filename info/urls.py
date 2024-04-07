from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_plant_info, name='display_plant_info'),
    path('plant_detail/<int:pk>', views.plant_detail, name='plant_detail'),
    path('add_plant/', views.add_plant, name='add_plant'),
    path('update_plant/<int:pk>', views.update_plant, name='update_plant'),
    path('delete_plant/<int:pk>', views.delete_plant, name='delete_plant'),
]