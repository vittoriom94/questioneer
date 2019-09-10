from django.db import models


# Create your models here.

class Exam(models.Model):
  exam_name = models.CharField(max_length=50)
  active = models.BooleanField(default=True)
  lastQuestion = models.IntegerField(default=0)


class Question(models.Model):
  question_text = models.CharField(max_length=600)
  exam = models.ForeignKey(Exam, on_delete=models.PROTECT)


class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  answer_text = models.CharField(max_length=600)
  correct = models.BooleanField(default=False)
