from django.urls import path
from . import views

urlpatterns = [
    path('obtener_clima/', views.obtener_clima, name='obtener_clima'),
]
