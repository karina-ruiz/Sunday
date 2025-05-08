from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.TextField()

    def __str__(self):
        return self.texto

class OpcionRespuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=255)
    valor = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.texto} (Valor: {self.valor})'

class RespuestaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    puntuacion_total = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.test.nombre}'

class RespuestaPregunta(models.Model):
    respuesta_usuario = models.ForeignKey(RespuestaUsuario, on_delete=models.CASCADE, related_name='respuestas')
    opcion = models.ForeignKey(OpcionRespuesta, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.opcion.pregunta.texto[:30]} → {self.opcion.texto}'
