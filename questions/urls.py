from django.urls import path

from . import views

app_name = 'questions'
urlpatterns = [
  path('', views.index, name="index"),
  path('insert_question/', views.insert_question, name="insert_question"),
  path('question/', views.question, name="question"),
  path('questions_list/', views.questions_list, name="questions_list"),
  path('exams/', views.exams, name="exams"),
]
