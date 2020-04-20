from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('round', views.rounds, name='round'),
    path('<int:quiz_id>', views.quizdetail, name='quizdetail'),
    path('<int:quiz_id>/', views.createquestion, name='createquestion'),
    path('', views.create, name='quiz/create'),

]
