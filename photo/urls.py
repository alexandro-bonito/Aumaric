from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Page d'accueil
    path('dashboard/', views.dashboard, name='dashboard'),
]
