from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<int:quiz_id>', views.quizdetail, name='quizdetail'),
    path('', views.create, name='quiz/create'),
    path('<int:quiz_id>/round', views.round, name='round'),
    # path('<int:quiz_id>/', views.createround, name='createround'),
    path('<int:quiz_id>/createround', views.createround, name='createround'),
    path('<int:quiz_id>/round/<int:round_id>/', views.rounddetail, name='rounddetail'),
    path('<int:quiz_id>/round/<int:round_id>/questions', views.questions, name='questions'),
    path('<int:quiz_id>/round/<int:round_id>/submitquestion', views.submitquestion, name='submitquestion'),

]
