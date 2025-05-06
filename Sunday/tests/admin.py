from django.contrib import admin
from .models import Categoria, Test, Pregunta, OpcionRespuesta, RespuestaUsuario, RespuestaPregunta

# Opciones de respuesta en línea dentro de cada pregunta
class OpcionRespuestaInline(admin.TabularInline):
    model = OpcionRespuesta
    extra = 2  # Cuántas opciones en blanco se muestran por defecto

# Configuración para las preguntas
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['texto', 'test', 'peso']
    inlines = [OpcionRespuestaInline]

# Preguntas en línea dentro del Test (opcional, para ver las preguntas del test en el admin)
class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1

# Configuración para los tests
class TestAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria']
    inlines = [PreguntaInline]

# Mostrar respuestas en la vista de usuario
class RespuestaPreguntaInline(admin.TabularInline):
    model = RespuestaPregunta
    extra = 0
    readonly_fields = ['opcion']

class RespuestaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'test', 'fecha', 'puntuacion_total']
    inlines = [RespuestaPreguntaInline]
    readonly_fields = ['usuario', 'test', 'fecha', 'puntuacion_total']

# Registro de modelos en el admin
admin.site.register(Categoria)
admin.site.register(Test, TestAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(RespuestaUsuario, RespuestaUsuarioAdmin)

