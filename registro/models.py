from django.db import models
from django.contrib.auth.models import User


EMOTION_CHOICES = [
    ('aburrimiento', 'Aburrimiento'),
    ('agotamiento', 'Agotamiento'),
    ('alegria', 'Alegría'),
    ('amor', 'Amor'),
    ('ansiedad', 'Ansiedad'),
    ('calma', 'Calma'),
    ('compasion', 'Compasión'),
    ('confusion', 'Confusión'),
    ('culpa', 'Culpa'),
    ('duda', 'Duda'),
    ('envidia', 'Envidia'),
    ('esperanza', 'Esperanza'),
    ('frustracion', 'Frustración'),
    ('gratitud', 'Gratitud'),
    ('indiferencia', 'Indiferencia'),
    ('inseguridad', 'Inseguridad'),
    ('interes', 'Interés'),
    ('ira', 'Ira'),
    ('motivacion', 'Motivación'),
    ('miedo', 'Miedo'),
    ('nostalgia', 'Nostalgia'),
    ('orgullo', 'Orgullo positivo'),
    ('seguridad', 'Seguridad'),
    ('soledad', 'Soledad'),
    ('sorpresa', 'Sorpresa'),
    ('tristeza', 'Tristeza'),
    ('vergüenza', 'Vergüenza'),
]


class EmotionQuestion(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class EmotionEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(EmotionQuestion, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES)


    INTENSITY_CHOICES = [
        (1, '1 - Muy baja'),
        (2, '2 - Baja'),
        (3, '3 - Moderada'),
        (4, '4 - Alta'),
        (5, '5 - Muy alta'),
    ]
    intensity = models.PositiveSmallIntegerField(choices=INTENSITY_CHOICES, default=3)


    def __str__(self):
        return f"{self.user.username} - {self.question.text[:20]} - {self.emotion} ({self.intensity}) - {self.date}"
