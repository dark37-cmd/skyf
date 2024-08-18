from django.shortcuts import render, redirect
from .models import Question, UserDetail
from django.http import JsonResponse
from .forms import QuizForm, UserDetailForm

def index(request):
    return render(request, 'main/index.html')


def become_a_skuf(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        if 'consent_checkbox' in request.POST:
            return redirect('start_test')
        else:
            return render(request, 'become-a-skuf/start_test.html', {
                'error': 'Необходимо согласие на обработку персональных данных.'
            })

    return render(request, 'become-a-skuf/start_test.html')

def start_test(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            total = questions.count()

            # Calculate score
            for question in questions:
                answer = form.cleaned_data.get(f'question_{question.id}')
                if answer and answer.is_correct:
                    score += 1

            # Проверка на максимальный балл
            if score == 2:
                # Если максимальный балл, перенаправляем на страницу благодарности
                return redirect('thank_you_view')
            else:
                # Если не набран максимальный балл, возвращаем форму с сообщением
                return render(request, 'become-a-skuf/unlucky.html', {
                    'form': form,
                    'error': 'Вы не набрали максимальный балл. Пожалуйста, попробуйте еще раз.'
                })

        else:
            # Если форма не валидна
            return render(request, 'become-a-skuf/quiz.html', {
                'form': form,
                'error': 'Некоторые ответы неверны. Попробуйте еще раз.'
            })

    else:
        form = QuizForm(questions=questions)

    return render(request, 'become-a-skuf/quiz.html', {'form': form})

def thank_you_view(request):
    return render(request, 'become-a-skuf/thank_you.html')

def submit_details(request):
    if request.method == 'POST':
        form = UserDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Ваши данные успешно отправлены. Спасибо!")
        else:
            return render(request, 'become-a-skuf/thank_you.html', {
                'form': form,
                'error': 'Пожалуйста, заполните форму правильно.'
            })
    else:
        form = UserDetailForm()
    return render(request, 'become-a-skuf/thank_you.html', {'form': form})

def unlucky(request):
    return render(request, 'become-a-skuf/unlucky.html')