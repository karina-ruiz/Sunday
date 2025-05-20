from django import forms
from .models import DiarioEntrada
from django_quill.forms import QuillFormField

class DiarioEntradaForm(forms.ModelForm):
    class Meta:
        model = DiarioEntrada
        fields = ['texto']
        labels = {
            'texto': 'Tu entrada de hoy',
        }
