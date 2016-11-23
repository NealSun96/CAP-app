from django.db import models
from django.conf import settings
from assignment.models import Assignment
from enrollment.models import Enrollment


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    enrollment = models.ForeignKey(Enrollment)
    assignment = models.ForeignKey(Assignment)
    # json formatted dictionary answers
    answers = models.TextField()
    time_taken = models.FloatField()
    score = models.IntegerField()
    completion_date = models.DateTimeField()
