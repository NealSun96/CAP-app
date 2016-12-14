from django.db import models
from answer.models import Answer
from knowledge_test.models import KnowledgeTest


class KnowledgeTestAnswer(Answer):
    knowledge_test = models.ForeignKey(KnowledgeTest)
    answers = models.TextField()
    time_taken = models.FloatField()
    first_score = models.IntegerField()
    final_score = models.IntegerField()
    completion_date = models.DateTimeField()
