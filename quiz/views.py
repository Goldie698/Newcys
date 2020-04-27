from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Quiz, Round, Question
from django.utils import timezone
from django import forms



# Create your views here.
def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizlist': quizzes})


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
        else:
            return render(request, 'quiz/create.html', {'error': ' All fields must be filled out'})
    else:
        return render(request, 'quiz/create.html')

def play(request):
    return render(request, 'quiz/play.html')

def playscreen(request):
    data = request.POST.copy()
    quizCode = data.get('quizCode')
    context = {'quizCode': quizCode}
    #need to get the code from the post request from the form
    return render(request, 'quiz/playscreen.html', context)

def quizdetail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    rounds = Round.objects.filter(quiz=quiz)
    questions = []
    if quiz.founder == request.user:
        return render(request, 'quiz/quizdetail.html', {'quiz': quiz, 'rounds': rounds})
    else:
        for r in rounds:
            question = Question.objects.filter(round=r)
            if question:
                questions.append(question)
        if questions.__len__() <= 0:
            return render(request, 'quiz/playquiz.html', {'quiz': quiz, 'rounds': rounds})
        else:
            return render(request, 'quiz/playquiz.html', {'quiz': quiz, 'rounds': rounds, 'questions': questions})


def round(request, quiz_id):
    if request.method != 'POST':
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        return render(request, 'quiz/round.html', {'quiz': quiz})
    # return redirect('quiz/round/')


def createround(request, quiz_id):
    if request.method == 'POST':
        if request.POST['title']:
            r = Round()
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            r.quiz = quiz
            r.title = request.POST['title']
            r.save()
            return redirect('round/' + str(r.id))
        else:
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            return render(request, 'quiz/round.html', {'quiz': quiz, 'error': ' All fields must be filled out'})
    else:
        return render(request, 'quiz/round.html')


def rounddetail(request, round_id, quiz_id):
    round = get_object_or_404(Round, pk=round_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(round=round)
    return render(request, 'quiz/rounddetail.html', {'round': round, 'quiz': quiz, 'questions': questions})


def questions(request, quiz_id, round_id):
    round = get_object_or_404(Round, pk=round_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz/questions.html', {'quiz': quiz, 'round': round})


def submitquestion(request, quiz_id, round_id):
    if request.method == 'POST':
        round = get_object_or_404(Round, pk=round_id)
        quiz = Quiz.objects.get(round=round)
        if request.POST['prompt'] and request.POST['answer']:
            q = Question()
            q.round = round
            q.prompt = request.POST['prompt']
            q.answer = request.POST['answer']
            q.save()
            questions = Question.objects.filter(round=round)
            return render(request, 'quiz/rounddetail.html', {'round': round, 'quiz': quiz, 'questions': questions})
        else:
            questions = Question.objects.filter(round=round)
            return render(request, 'quiz/questions.html', {'round': round, 'quiz': quiz, 'questions': questions,
                                                           'error': ' All fields must be filled out'})
    else:
        return render(request, 'quiz/questions.html')


def editquiz(request):
    quizzes = Quiz.objects.filter(founder=request.user)
    return render(request, 'quiz/editquiz.html', {'quizzes': quizzes})


# def playquiz(request, q_id):
#     if request.method == 'POST':
#         question = get_object_or_404(Question, pk=q_id)
#         # questions = Question.objects.filter(round=round)
#         answer = request.POST['answer' + str(q_id)]
#         print(answer)
#         if question.answer == answer:
#             # form = request.POST
#             return redirect(request.META.get('HTTP_REFERER', {'answer': answer}))
#         else:
#             pass
