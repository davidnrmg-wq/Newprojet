from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from app.views import index, historico, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index),
    path('historico/', historico),
    path('dashboard/', dashboard),

    path('login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('logout/', auth_views.LogoutView.as_view()),
]