from django.urls import path
from . import views

urlpatterns = [
    path('playscreen', views.playscreen, name='playscreen'),
    path('play', views.play, name='play'),
    path('create', views.create, name='create'),
    path('<int:quiz_id>', views.quizdetail, name='quizdetail'),
    path('', views.create, name='quiz/create'),
    path('editquiz', views.editquiz, name='quiz/editquiz'),
    # path('<int:q_id>/playquiz', views.playquiz, name='quiz/playquiz'),
    path('<int:quiz_id>/round', views.round, name='round'),
    path('<int:quiz_id>/createround', views.createround, name='createround'),
    path('<int:quiz_id>/round/<int:round_id>/', views.rounddetail, name='rounddetail'),
    path('<int:quiz_id>/round/<int:round_id>/questions', views.questions, name='questions'),
    path('<int:quiz_id>/round/<int:round_id>/submitquestion', views.submitquestion, name='submitquestion'),

]
