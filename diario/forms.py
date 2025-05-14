from django import forms
from .models import DiarioEntrada

class DiarioEntradaForm(forms.ModelForm):
    class Meta:
        model = DiarioEntrada
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Escribe cómo fue tu día...',
                'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring focus:ring-amber-300'
            })
        }
        labels = {
            'texto': 'Tu entrada de hoy',
        }
