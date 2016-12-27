from django.db import models
from enrollment.models import Enrollment


class KnowledgeTestFirstScore(models.Model):
    enrollment = models.ForeignKey(Enrollment)
    first_score = models.IntegerField()
