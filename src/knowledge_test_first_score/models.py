from django.db import models
from enrollment.models import Enrollment


class KnowledgeTestFirstScore(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    first_score = models.IntegerField()
