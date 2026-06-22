from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('historico/', views.historico, name='historico'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
