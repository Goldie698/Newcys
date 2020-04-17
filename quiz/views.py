from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, Round, Questions
from django.utils import timezone


# Create your views here.
def home(request):
    return render(request, 'quiz/home.html')


@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title']:
            quiz = Quiz()
            quiz.title = request.POST['title']
            quiz.private = True
            quiz.pub_date = timezone.datetime.now()
            quiz.participants = 0
            quiz.founder = request.user
            quiz.save()
            return redirect('/quiz/' + str(quiz.id))
            # return render(request, 'quiz/questions.html')
            # return redirect('home')
        else:
            return render(request, 'quiz/create.html', {'error': ' All fields must be filled out'})
    else:
        return render(request, 'quiz/create.html')


# def rounds(request):
    # round1 = get_object_or_404(Quiz, pk=round_id)
    # return render(request, 'quiz/round.html')


def createrounds(request, quiz_id):
    if request.method == 'POST':
        if request.POST['title']:
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            r = Round()
            r.title = request.POST['title']
            r.quiz = quiz
            r.save()
            return render('/round/' + str(r.id))
        else:
            return render(request, 'quiz/quizdetail.html', {'error': ' All fields must be filled out'})
    else:
        return render(request, 'quiz/quizdetail.html')


def quizdetail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz/quizdetail.html', {'quiz': quiz})
#
# def questions(request):
#     ques = get_object_or_404(Round, pk=quiz_id)
#     return render(request, 'quiz/questions.html')
