from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

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
