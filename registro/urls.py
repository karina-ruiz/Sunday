from django.urls import path
from . import views
from django.shortcuts import render


urlpatterns = [
    path('registrar/', views.register_emotions, name='register_emotions'),
    path('ya-registrado/', lambda request: render(request, 'registro/emotion_already_submitted.html'), name='emotion_already_submitted'),
    path('resultados/', views.ver_resultados, name='ver_resultados'),
    path('resultados-historicos/', views.resultados_historicos, name='resultados_historicos'),
    path('resultados/dia/', views.resultados_dia, name='resultados_dia'),
    path('resultados/semana/', views.resultados_semana, name='resultados_semana'),
]
