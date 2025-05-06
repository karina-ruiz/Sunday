from django.shortcuts import render, get_object_or_404
from .models import Test, Pregunta
from asgiref.sync import sync_to_async

def lista_tests(request):
    tests = Test.objects.all()
    return render(request, 'tests/lista_tests.html', {'tests': tests})

def tomar_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    preguntas = test.preguntas.prefetch_related('opciones')  # Accede a las preguntas y sus opciones

    return render(request, 'tests/tomar_test.html', {
        'test': test,
        'preguntas': preguntas,
    })

@sync_to_async
def obtener_test_con_preguntas(test_id):
    test = get_object_or_404(Test, id=test_id)
    preguntas = test.preguntas.prefetch_related('opciones').all()
    return test, preguntas

async def tomar_test(request, test_id):
    test, preguntas = await obtener_test_con_preguntas(test_id)

    if request.method == 'POST':
        puntuacion_total = 0

        for pregunta in preguntas:
            valor = request.POST.get(f"pregunta_{pregunta.id}")
            if valor:
                puntuacion_total += int(valor) * pregunta.peso


# Clasificación por rangos de puntuación
        if puntuacion_total <= 10:
            resultado = f"Tu rango de respuestas es mínimo, por lo cual estás libre de {test.nombre}."
        elif 11 <= puntuacion_total <= 20:
            resultado = f"Tu rango de respuestas es poco preocupante, por lo cual deberías tomarlo en cuenta {test.nombre}."
        elif 21 <= puntuacion_total <= 30:
            resultado = f"Tu rango de respuestas es poco alto, por lo cual ocupas ayuda psicológica {test.nombre}."
        else:  # 31 o más
            resultado = f"Tu rango de respuestas es muy alto, por lo cual necesitas ayuda {test.nombre}."

        return render(request, 'tests/resultados.html', {
            'test': test,
            'puntuacion_total': puntuacion_total,
            'resultado': resultado
        })

    return render(request, 'tests/tomar_test.html', {
        'test': test,
        'preguntas': preguntas
    })

