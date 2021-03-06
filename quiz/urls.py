from django.urls import path

from pubquiz import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
                  path('playscreen', views.playscreen, name='playscreen'),
                  path('<int:round_id>/seeAnswers', views.seeAnswers, name='quiz/seeAnswers'),
                  path('enterQuizCode', views.enterQuizCode, name='enterQuizCode'),
                  path('create', views.create, name='create'),
                  path('<int:quiz_id>', views.quizdetail, name='quizdetail'),
                  path('', views.create, name='quiz/create'),
                  path('editquiz', views.editquiz, name='quiz/editquiz'),
                  path('<int:round_id>/playquiz', views.playquiz, name='quiz/playquiz'),
                  path('<int:quiz_id>/round', views.round, name='round'),
                  path('<int:quiz_id>/createround', views.createround, name='createround'),
                  path('<int:quiz_id>/round/<int:round_id>/', views.rounddetail, name='rounddetail'),
                  path('<int:quiz_id>/round/<int:round_id>/questions', views.questions, name='questions'),
                  path('<int:quiz_id>/round/<int:round_id>/questiontype', views.questiontype,
                       name='questiontype'),
                  path('<int:quiz_id>/round/<int:round_id>/submitquestion', views.submitquestion,
                       name='submitquestion'),
                  path('<int:quiz_id>/round/<int:round_id>/submitmcq', views.submitmcq,
                       name='submitmcq'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
