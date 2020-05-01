from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Round, Question, QuizTakers, Response, RoundTakers
from django.utils import timezone
import re
from .forms import QuestionForm, MCQuestionForm
from mcq.models import MCQuestion, Choice, MCQResponse


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


@login_required(login_url='login')
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
            if QuizTakers.objects.filter(user=request.user, quiz=quiz).exists():
                quiztaker = QuizTakers.objects.filter(user=request.user, quiz=quiz).first()
                return render(request, 'quiz/playquiz.html', {'quiz': quiz, 'rounds': rounds})
            else:
                quiztaker = QuizTakers()
                quiztaker.quiz = quiz
                quiztaker.user = request.user
                quiztaker.save()
                return render(request, 'quiz/playquiz.html', {'quiz': quiz, 'rounds': rounds})
    else:
        return render(request, 'quiz/enterQuizCode.html', {'error': 'you must enter a code'})


@login_required(login_url='login')
def quizdetail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    rounds = Round.objects.filter(quiz=quiz)
    if quiz.founder == request.user:
        return render(request, 'quiz/quizdetail.html', {'quiz': quiz, 'rounds': rounds})
    else:
        if QuizTakers.objects.filter(user=request.user, quiz=quiz).exists():
            quiztaker = QuizTakers.objects.filter(user=request.user, quiz=quiz).first()
            return render(request, 'quiz/playquiz.html', {'quiz': quiz, 'rounds': rounds})
        else:
            quiztaker = QuizTakers()
            quiztaker.quiz = quiz
            quiztaker.user = request.user
            quiztaker.save()
            return render(request, 'quiz/playquiz.html', {'quiz': quiz, 'rounds': rounds})


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
    mcquestions = MCQuestion.objects.filter(round=round)
    questions = Question.objects.filter(round=round)
    return render(request, 'quiz/rounddetail.html',
                  {'round': round, 'quiz': quiz, 'questions': questions, 'mcquestions': mcquestions})


def questions(request, quiz_id, round_id):
    round = get_object_or_404(Round, pk=round_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz/questions.html', {'quiz': quiz, 'round': round})


def submitquestion(request, quiz_id, round_id):
    round = get_object_or_404(Round, pk=round_id)
    quiz = Quiz.objects.get(round=round)
    mcquestions = MCQuestion.objects.filter(round=round)
    if request.method == 'POST':
        if request.POST['prompt'] and request.POST['answer']:
            q = Question()
            q.round = round
            q.prompt = request.POST['prompt']
            q.answer = request.POST['answer']
            q.save()
            questions = Question.objects.filter(round=round)
            return render(request, 'quiz/rounddetail.html',
                          {'quiz': quiz, 'round': round, 'questions': questions})
        else:
            # print(request.POST)
            questions = Question.objects.filter(round=round)
            return render(request, 'quiz/questions.html', {'round': round, 'quiz': quiz, 'questions': questions,
                                                           'error': ' All fields must be filled out'})
    else:
        return render(request, 'quiz/questions.html')


def submitmcq(request, quiz_id, round_id):
    if request.method == 'POST':
        round = Round.objects.get(pk=round_id)
        quiz = Quiz.objects.get(pk=quiz_id)
        if request.POST['prompt'] and request.POST.get('choice_text1') and request.POST.get(
                'choice_text2') and request.POST.get('choice_text3'):
            choice1 = request.POST.get('choice_text1')
            choice2 = request.POST.get('choice_text2')
            choice3 = request.POST.get('choice_text3')
            mcquestion = MCQuestion()
            mcquestion.prompt = request.POST['prompt']
            mcquestion.round = round
            mcquestion.save()
            if request.POST.get('correct1'):
                mcquestion.choice_set.create(choice_text=choice1, correct=True)
            else:
                mcquestion.choice_set.create(choice_text=choice1, correct=False)
            if request.POST.get('correct2'):
                mcquestion.choice_set.create(choice_text=choice2, correct=True)
            else:
                mcquestion.choice_set.create(choice_text=choice2, correct=False)
            if request.POST.get('correct3'):
                mcquestion.choice_set.create(choice_text=choice3, correct=True)
            else:
                mcquestion.choice_set.create(choice_text=choice3, correct=False)
            mcquestion.save()
            mcquestions = MCQuestion.objects.filter(round=round)
            return render(request, 'quiz/rounddetail.html',
                          {'quiz': quiz, 'round': round, 'mcquestions': mcquestions})
        else:
            error = 'All fields must be filled! Make sure you pick an answer'
            return render(request, 'quiz/questions.html',
                          {'quiz': quiz, 'round': round, 'mcq': 'mcq', 'error_answer': error})


def questiontype(request, quiz_id, round_id):
    round = get_object_or_404(Round, pk=round_id)
    quiz = Quiz.objects.get(round=round)
    mcquestions = MCQuestion.objects.filter(round=round)
    questions = Question.objects.filter(round=round)
    if request.method == 'POST':
        if request.POST['question_types']:
            type = request.POST['question_types']
            if type == 'Free text' and len(mcquestions) <= 0:
                return render(request, 'quiz/questions.html',
                              {'quiz': quiz
                                  , 'round': round, 'free': 'free'})
            elif type == 'Multiple choice' and len(questions) <= 0:
                return render(request, 'quiz/questions.html', {'quiz': quiz, 'round': round, 'mcq': 'mcq'})
            else:
                error = 'Each round can only have one type of questions'
                form = QuestionForm()
                return render(request, 'quiz/questions.html',
                              {'quiz': quiz, 'round': round, 'error_type': error, 'form': form})
        else:
            error = 'You must choose question type'
            return render(request, 'quiz/questions.html', {'quiz': quiz, 'round': round, 'error': error})
    elif request.method == 'GET':
        form = QuestionForm()
        return render(request, 'quiz/questions.html', {'round': round, 'quiz': quiz, 'form': form})


@login_required(login_url='login')
def editquiz(request):
    quizzes = Quiz.objects.filter(founder=request.user)
    return render(request, 'quiz/editquiz.html', {'quizzes': quizzes})


def playquiz(request, round_id):
    round = get_object_or_404(Round, pk=round_id)
    quiztaker = QuizTakers.objects.filter(user=request.user, quiz=round.quiz)
    if quiztaker:
        count = 0
        questions = Question.objects.filter(round=round)
        mcquestions = MCQuestion.objects.filter(round=round)
        if request.method == 'GET':
            return render(request, 'quiz/playround.html', {'round': round, 'mcforms': mcquestions})
        elif request.method == 'POST':
            for mcq in mcquestions:
                if request.POST.get(str(mcq.id)):
                    choice = Choice.objects.get(pk=request.POST[str(mcq.id)])
                    if MCQResponse.objects.filter(quiztaker=quiztaker.first(), question=mcq).exists():
                        response = MCQResponse.objects.filter(quiztaker=quiztaker.first(), question=mcq).first()
                        response.answer = choice.choice_text
                        response.save()
                    else:
                        response = MCQResponse()
                        response.question = mcq
                        response.quiztaker = quiztaker.first()
                        response.answer = choice.choice_text
                        response.save()
                    if mcq.check_if_correct(request.POST[str(mcq.id)]):
                        count += 1
                        print('Correct!')
                    else:
                        print('Incorrect!')
                # TODO add score functionality
                else:
                    error = 'You must choose one answer per question'
                    return render(request, 'playround.html',
                                  {'round': round, 'mcforms': mcquestions, 'error_choices': error})
            for q in questions:
                answerId = q.id
                if request.POST[str(answerId)]:
                    answer = str(q.answer)
                    useranswer = request.POST[str(answerId).lower()]
                    if Response.objects.filter(quiztaker=quiztaker.first(), question=q).exists():
                        response = Response.objects.filter(quiztaker=quiztaker.first(), question=q).last()
                        response.answer = useranswer
                        response.save()
                    else:
                        response = Response()
                        response.quiztaker = quiztaker.first()
                        response.question = q
                        response.answer = useranswer
                        response.save()
                        if re.findall('(?i)' + answer, useranswer):
                            count += 1
                            print('Found the right answer')
                        else:
                            print('Incorrect answer' + str(q.prompt))
            if RoundTakers.objects.filter(user=request.user, round=round).exists():
                print('have roundtaker')
                roundtaker = RoundTakers.objects.filter(user=request.user, round=round).first()
                roundtaker.score = count
                roundtaker.save()
            else:
                print('no roundtaker')
                roundtaker = RoundTakers()
                roundtaker.round = round
                roundtaker.user = request.user
                roundtaker.score = count
                roundtaker.save()
            quiz = round.quiz
            rounds = Round.objects.filter(quiz=quiz)
            return render(request, 'quiz/playquiz.html', {'quiz': quiz, 'rounds': rounds
                , 'played': round})
    else:
        print('Something went wrong')


def seeAnswers(request, round_id):
    round = get_object_or_404(Round, pk=round_id)
    quizQuestions = Question.objects.filter(round=round)
    quiz = round.quiz
    questions = {}
    quizTaker = QuizTakers.objects.get(user=request.user, quiz=quiz)
    roundTaker = RoundTakers.objects.get(user=request.user, round=round)
    if quizQuestions:
        for q in quizQuestions:
            answers = []
            answers.append(q.answer)
            if Response.objects.filter(question=q, quiztaker=quizTaker).exists():
                answers.append(Response.objects.get(question=q, quiztaker=quizTaker).answer)
                if re.findall('(?i)' + answers[0], answers[1]):
                    answers.append('yes')
                else:
                    answers.append('no')
                questions[q.prompt] = answers
            # return render(request, 'quiz/seeAnswers.html', {'round': round, 'questions': questions})
            else:
                error = 'You did not provide answers!'
                return render(request, 'quiz/seeAnswers.html',
                              {'quiz': quiz, 'round': round, 'questions': questions, 'error': error})
    else:
        quizQuestions = MCQuestion.objects.filter(round=round)
        for mcq in quizQuestions:
            answers = []
            choices = mcq.choice_set.all()
            for c in choices:
                if c.correct:
                    answers.append(c.choice_text)
            answers.append(MCQResponse.objects.get(question=mcq, quiztaker=quizTaker).answer)
            if re.findall('(?i)' + answers[0], answers[1]):
                answers.append('yes')
            else:
                answers.append('no')
            questions[mcq.prompt] = answers
    roundScore = []
    roundScore.append(roundTaker.score)
    roundScore.append(len(quizQuestions))
    return render(request, 'quiz/seeAnswers.html',
                  {'quiz': quiz, 'round': round, 'questions': questions, 'score': roundScore})
