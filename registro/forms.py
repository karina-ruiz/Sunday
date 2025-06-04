from django import forms
from .models import EmotionQuestion, EMOTION_CHOICES

INTENSITY_CHOICES = [
    (1, '1 - Muy baja'),
    (2, '2 - Baja'),
    (3, '3 - Moderada'),
    (4, '4 - Alta'),
    (5, '5 - Muy alta'),
]

class DynamicEmotionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DynamicEmotionForm, self).__init__(*args, **kwargs)
        questions = EmotionQuestion.objects.all()[:5]

        for question in questions:
            emotion_field = f"question_{question.id}_emotion"
            intensity_field = f"question_{question.id}_intensity"

            self.fields[emotion_field] = forms.ChoiceField(
                label=question.text,
                choices=EMOTION_CHOICES,
                widget=forms.Select(attrs={'class': 'form-control'})
            )
            self.fields[emotion_field].question = question  
            self.fields[intensity_field] = forms.ChoiceField(
                label="Intensidad",
                choices=INTENSITY_CHOICES,
                widget=forms.Select(attrs={'class': 'form-control'})
            )
