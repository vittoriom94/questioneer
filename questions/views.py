import random

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.defaulttags import register

from questions.models import Answer, Question, Exam


def index(request):
  return HttpResponse("Hello, world. You're at questions index")


def insert_question(request):
  context = dict()
  if request.method == 'POST':
    question_text = request.POST['question']
    exam_id = request.POST['exam']
    exam = get_object_or_404(Exam, pk=exam_id)
    question = Question(question_text=question_text, exam=exam)
    question.save()
    for i in range(1, 5):
      answer_text = request.POST['answer' + str(i)]
      correct = int(request.POST['correct']) == i
      answer = Answer(answer_text=answer_text, correct=correct, question=question)
      answer.save()
    context['inserted'] = True
  exams = Exam.objects.all()
  context['exams'] = exams
  return render(request, 'questions/insert_question.html', context)


def question(request):
  context = dict()
  questions = Question.objects.filter(exam__active=True)
  if not questions:
    return render(request, 'questions/question.html')
  question = random.choice(questions)
  context['question'] = question
  answers = Answer.objects.filter(question=question)
  context['answers'] = answers
  return render(request, 'questions/question.html', context)


def questions_list(request):
  if request.method == 'POST':
    question_id = request.POST['delete']
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
  context = dict()
  questions = Question.objects.all()
  context['questions'] = questions
  context['answers'] = dict()
  for question in questions:
    question_id = question.id
    context['answers'][question_id] = Answer.objects.filter(question=question)
  return render(request, 'questions/questions_list.html', context)


@register.filter
def get_item(dictionary, key):
  return dictionary.get(key)


def exams(request):
  context = dict()
  if request.method == 'POST':
    if 'delete' in request.POST:
      exam_id = request.POST['delete']
      exam = get_object_or_404(Exam, pk=exam_id)
      exam.delete()
    elif 'enable' in request.POST:
      exam_id = request.POST['enable']
      exam = get_object_or_404(Exam, pk=exam_id)
      exam.active = not exam.active
      exam.save()
    else:
      exam_name = request.POST['exam']
      active = 'active' in request.POST
      exam = Exam(exam_name=exam_name, active=active)
      exam.save()
      context['inserted'] = True
  context['exams'] = Exam.objects.all()
  return render(request, 'questions/exams.html', context)
