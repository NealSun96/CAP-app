from django.db import models
from answer.models import Answer


class Diagnosis(Answer):
    self_diagnosis = models.TextField()
    other_diagnosis = models.TextField()
    completion_date = models.DateTimeField()
