from django.db import models
from enrollment.models import Enrollment


class KnowledgeTestStart(models.Model):
    enrollment = models.ForeignKey(Enrollment)
    start_time = models.DateTimeField(blank=True, null=True)
