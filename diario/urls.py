from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='diario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('diario/nueva/', views.nueva_entrada, name='nueva_entrada'),
    path('diario/', views.ver_entradas, name='ver_entradas'),
]
