from django.db import models
from assignment.models import Assignment
from question.models import Question


class QuestionOrdered(models.Model):
    ordering = models.IntegerField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        ordering = ['ordering']
