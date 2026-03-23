"""
URLs pour les pages frontend
"""

from django.urls import path
from . import views_frontend

app_name = 'sdau'

urlpatterns = [
    path('', views_frontend.index, name='index'),
    path('login/', views_frontend.login_page, name='login'),
    path('register/', views_frontend.register_page, name='register'),
    path('carte/', views_frontend.carte, name='carte'),
]
