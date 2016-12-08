from django.db import models
from knowledge_test.models import KnowledgeTest
from question.models import Question


class QuestionOrdered(models.Model):
    ordering = models.IntegerField()
    test = models.ForeignKey(KnowledgeTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        ordering = ['ordering']
