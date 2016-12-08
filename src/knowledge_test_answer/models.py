from django.db import models
from answer.models import Answer


class KnowledgeTestAnswer(Answer):
    answers = models.TextField()
    time_taken = models.FloatField()
    first_score = models.IntegerField()
    final_score = models.IntegerField()
    completion_date = models.DateTimeField()
