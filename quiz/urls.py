from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('round', views.rounds, name='round'),
    path('<int:quiz_id>/', views.createrounds, name='createrounds'),
    path('', views.create, name='quiz/create'),

    path('<int:quiz_id>', views.quizdetail, name='quizdetail'),

]
