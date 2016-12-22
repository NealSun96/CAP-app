from django.db import models
from enrollment.models import Enrollment


class Answer(models.Model):
    enrollment = models.ForeignKey(Enrollment)

    class Meta:
        abstract = True
