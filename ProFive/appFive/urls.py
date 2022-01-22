from django.contrib import admin
from django.urls import path
from appFive import views

# TEMPLATE URLs
app_name = 'appFive'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login')
]