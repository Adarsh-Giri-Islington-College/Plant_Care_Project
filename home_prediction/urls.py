from django.contrib import admin
from django.urls import path
from home_prediction import views

urlpatterns = [
    path('prediction_history/', views.prediction_history, name='prediction_history'),
    ]