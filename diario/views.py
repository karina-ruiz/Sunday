from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import DiarioEntradaForm
from .models import DiarioEntrada

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # Loguea automáticamente después de registrar
            return redirect('ver_entradas')  # O donde desees
    else:
        form = UserCreationForm()
    return render(request, 'diario/registro.html', {'form': form})



@login_required
def nueva_entrada(request):
    if request.method == 'POST':
        form = DiarioEntradaForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.usuario = request.user
            entrada.save()
            return redirect('ver_entradas')  # Redirige a una página donde se muestren todas las entradas
    else:
        form = DiarioEntradaForm()

    return render(request, 'diario/nueva_entrada.html', {'form': form})


@login_required
def ver_entradas(request):
    entradas = DiarioEntrada.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'diario/ver_entradas.html', {'entradas': entradas})