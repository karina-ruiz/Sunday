from django.db import models
from django.contrib.auth.models import User

class DiarioEntrada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.fecha_creacion.strftime("%Y-%m-%d %H:%M")}'
