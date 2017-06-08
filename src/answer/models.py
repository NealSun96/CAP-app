from django.db import models
from enrollment.models import Enrollment


class Answer(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)

    class Meta:
        abstract = True
