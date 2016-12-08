from django.db import models
from django.conf import settings
from enrollment.models import Enrollment


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    enrollment = models.ForeignKey(Enrollment)

    class Meta:
        abstract = True
