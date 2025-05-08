from django.contrib import admin
from .models import Test, Pregunta, OpcionRespuesta


class OpcionRespuestaInline(admin.TabularInline):
    model = OpcionRespuesta
    extra = 4  
    fields = ('texto', 'valor')  


class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'test')  
    inlines = [OpcionRespuestaInline]  


class TestAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')  


admin.site.register(Test, TestAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(OpcionRespuesta) 
