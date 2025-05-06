from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.lista_tests, name='lista_tests'),
    path('tests/<int:test_id>/', views.tomar_test, name='tomar_test'),
]
