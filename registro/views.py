import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DynamicEmotionForm
from .models import EmotionEntry, EmotionQuestion, EMOTION_CHOICES
from django.db.models import Avg
import json


@login_required
def register_emotions(request):
    today = datetime.date.today()
    user = request.user
    questions_today = EmotionQuestion.objects.all()[:5]

    already_answered = EmotionEntry.objects.filter(
        user=user,
        question__in=questions_today,
        date=today
    ).exists()

    if already_answered:
        messages.info(request, "Ya has registrado tus emociones hoy.")
        return redirect('emotion_already_submitted')

    if request.method == 'POST':
        form = DynamicEmotionForm(request.POST)
        if form.is_valid():
            for field_name in form.cleaned_data:
                if field_name.endswith('_emotion'):
                    question_id = int(field_name.split('_')[1])
                    question = EmotionQuestion.objects.get(id=question_id)
                    emotion = form.cleaned_data[field_name]
                    intensity = int(form.cleaned_data[f'question_{question_id}_intensity'])

                    EmotionEntry.objects.create(
                        user=user,
                        question=question,
                        emotion=emotion,
                        intensity=intensity,
                        date=today
                    )

            messages.success(request, "Tus emociones han sido registradas.")
            return redirect('emotion_success')
    else:
        form = DynamicEmotionForm()

    return render(request, 'registro/register.html', {'form': form})


@login_required
def register_emotions(request):
    today = datetime.date.today()
    user = request.user

    questions_today = EmotionQuestion.objects.all()[:5]
    already_answered = EmotionEntry.objects.filter(
        user=user,
        question__in=questions_today,
        date=today
    ).exists()

    if already_answered:
        messages.info(request, "Ya has registrado tus emociones hoy.")
        return redirect('emotion_already_submitted')

    if request.method == 'POST':
        form = DynamicEmotionForm(request.POST)
        if form.is_valid():
            for question in questions_today:
                emotion_field = f"question_{question.id}_emotion"
                intensity_field = f"question_{question.id}_intensity"

                emotion = form.cleaned_data.get(emotion_field)
                intensity = form.cleaned_data.get(intensity_field)

                
                if not EmotionEntry.objects.filter(user=user, question=question, date=today).exists():
                    EmotionEntry.objects.create(
                        user=user,
                        question=question,
                        emotion=emotion,
                        intensity=intensity
                    )

            messages.success(request, "Tus emociones han sido registradas.")
            return redirect('ver_resultados')
    else:
        form = DynamicEmotionForm()

    return render(request, 'registro/register.html', {'form': form})


@login_required
def ver_resultados(request):
    today = datetime.date.today()
    entries = EmotionEntry.objects.filter(user=request.user, date=today)

    labels = [entry.emotion.capitalize() for entry in entries]
    data = [entry.intensity for entry in entries]

    return render(request, 'registro/resultados.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    })

@login_required
def resultados_historicos(request):
    user = request.user
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=6) 

    entries = EmotionEntry.objects.filter(
        user=user,
        date__range=[start_date, today]
    )

    
    data_dict = {}

    for single_date in (start_date + datetime.timedelta(n) for n in range(7)):
        data_dict[single_date] = {}

    for entry in entries:
        fecha = entry.date
        emocion = entry.emotion
        intensidad = entry.intensity

        if emocion not in data_dict[fecha]:
            data_dict[fecha][emocion] = []
        data_dict[fecha][emocion].append(intensidad)

   
    for fecha, emociones in data_dict.items():
        for emocion, intensidades in emociones.items():
            avg_intensity = sum(intensidades) / len(intensidades)
            data_dict[fecha][emocion] = round(avg_intensity, 2)

    
    labels = [fecha.strftime('%d/%m') for fecha in data_dict.keys()]

    
    emociones_list = [choice[0] for choice in EMOTION_CHOICES]

    datasets = []
    colors = ['rgba(54, 162, 235, 0.5)', 'rgba(255, 99, 132, 0.5)', 'rgba(255, 206, 86, 0.5)', 'rgba(75, 192, 192, 0.5)']  # colores para cada emoción

    for i, emocion in enumerate(emociones_list[:4]):  
        data = []
        for fecha in data_dict.keys():
            valor = data_dict[fecha].get(emocion, 0)
            data.append(valor)
        datasets.append({
            'label': emocion.capitalize(),
            'data': data,
            'backgroundColor': colors[i % len(colors)],
            'borderColor': colors[i % len(colors)].replace('0.5', '1'),
            'borderWidth': 1
        })

    context = {
        'labels': labels,
        'datasets': datasets,
    }

    return render(request, 'registro/resultados_historicos.html', context)



@login_required
def resultados_dia(request):
    date_str = request.GET.get('date')
    if date_str:
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = datetime.date.today()
    else:
        date = datetime.date.today()

    entries = EmotionEntry.objects.filter(user=request.user, date=date)

   
    emotion_data = {}
    for entry in entries:
        emocion = entry.emotion
        emotion_data.setdefault(emocion, []).append(entry.intensity)

    labels = []
    intensities = []
    for emocion, intensities_list in emotion_data.items():
        labels.append(emocion.capitalize())
        avg_intensity = sum(intensities_list) / len(intensities_list)
        intensities.append(round(avg_intensity, 2))

    return render(request, 'registro/resultados_dia.html', {
        'labels': labels,
        'intensities': intensities,
        'date': date,
    })



@login_required
def resultados_semana(request):
    today = datetime.date.today()
    start_week = today - datetime.timedelta(days=today.weekday())  
    end_week = start_week + datetime.timedelta(days=6)  

    entries = EmotionEntry.objects.filter(user=request.user, date__range=[start_week, end_week])

   
    emotion_data = {}
    for entry in entries:
        emocion = entry.emotion
        emotion_data.setdefault(emocion, []).append(entry.intensity)

    labels = []
    avg_intensities = []
    for emocion, intensities_list in emotion_data.items():
        labels.append(emocion.capitalize())
        avg_intensity = sum(intensities_list) / len(intensities_list)
        avg_intensities.append(round(avg_intensity, 2))

    return render(request, 'registro/resultados_semana.html', {
        'labels': labels,
        'avg_intensities': avg_intensities,
        'start_week': start_week,
        'end_week': end_week,
    })
