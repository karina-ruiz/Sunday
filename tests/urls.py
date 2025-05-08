from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.pagina_principal, name='inicio'),
    path('tests/', views.lista_tests, name='lista_tests'),
    path('tests/<int:test_id>/', views.tomar_test, name='tomar_test'),
]
