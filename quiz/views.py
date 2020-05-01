from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Round, Question, QuizTakers, RoundTakers, Response
from django.utils import timezone
import re


# Create your views here.
def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizlist': quizzes})


@login_required(login_url='login')
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


def enterQuizCode(request):
    return render(request, 'quiz/enterQuizCode.html')


def playscreen(request):
    if request.POST['quizCode']:
        try:
            quiz = Quiz.objects.get(pk=request.POST['quizCode'])
        except Quiz.DoesNotExist:
            return render(request, 'quiz/enterQuizCode.html', {'error': 'This Quiz does not exist'})

        rounds = Round.objects.filter(quiz=quiz)
        if quiz.founder == request.user:
            return render(request, 'quiz/enterQuizCode.html', {'error': 'you cannot play your own quiz'})
        else:
            quiztaker = QuizTakers()
            quiztaker.quiz = quiz
            quiztaker.user = request.user
            quiztaker.save()
            return render(request, 'quiz/playquiz.html', {'quiz': quiz, 'rounds': rounds, 'quiztaker': quiztaker})
    else:
        return render(request, 'quiz/enterQuizCode.html', {'error': 'you must enter a code'})


def quizdetail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    rounds = Round.objects.filter(quiz=quiz)
    if quiz.founder == request.user:
        return render(request, 'quiz/quizdetail.html', {'quiz': quiz, 'rounds': rounds})
    else:
        quiztaker = QuizTakers()
        quiztaker.quiz = quiz
        quiztaker.user = request.user
        quiztaker.save()
        return render(request, 'quiz/playquiz.html', {'quiz': quiz, 'rounds': rounds, 'quiztaker': quiztaker})


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


@login_required(login_url='login')
def editquiz(request):
    quizzes = Quiz.objects.filter(founder=request.user)
    return render(request, 'quiz/editquiz.html', {'quizzes': quizzes})


def playquiz(request, round_id):
    round = get_object_or_404(Round, pk=round_id)
    quiztaker = QuizTakers.objects.filter(user=request.user, quiz=round.quiz)
    print(quiztaker)
    if quiztaker:
        questions = Question.objects.filter(round=round)
        count = 0
        if request.method == 'GET':
            return render(request, 'quiz/playround.html', {'round': round, 'questions': questions})
        elif request.method == 'POST':
            userResponses = []
            for q in questions:
                answerId = q.id
                # print(request.POST.get(str(answerId), None))
                if request.POST[str(answerId)]:
                    answer = str(q.answer)
                    useranswer = request.POST[str(answerId).lower()]
                    response = Response()
                    response.quiztaker = quiztaker.first()
                    response.question = q
                    response.answer = useranswer
                    response.save()
                    userResponses.append(response)
                    if re.findall('(?i)' + answer, useranswer):
                        count += 1
                        print('Found the right answer')
                    else:
                        print('Incorrect answer' + str(q.prompt))
        roundtaker = RoundTakers()
        roundtaker.round = round
        roundtaker.user = request.user
        roundtaker.score = count
        roundtaker.save()
        quiz = round.quiz
        count2 = (count / len(questions) * 100)
        # round.score = count2
        # round.save()
        rounds = Round.objects.filter(quiz=quiz)
        return render(request, 'quiz/playquiz.html',
                      {'quiz': quiz, 'rounds': rounds,
                       'answers': 'Result: ' + str(count) + '/' + str(len(questions)), 'played': round,
                       'len': str(len(questions)), 'responses': userResponses})
    else:
        print('Something went wrong')

def seeAnswers(request, round_id):
    round = get_object_or_404(Round, pk=round_id)
    # print(round.id)
    # quiz = round.quiz
    questions = Question.objects.filter(round=round)
    # responses = []
    # quizTaker=QuizTakers.objects.get(user=request.user, quiz=quiz)
    # for q in questions:
    #     responses.append(Response.objects.get(question=q, quiztaker=quizTaker))
    # print(responses)
    # return render(request, 'quiz/seeAnswers.html', {'quiz': quiz, 'rounds': rounds,'responses': responses})
    return render(request, 'quiz/seeAnswers.html', {'round': round, 'questions': questions})
