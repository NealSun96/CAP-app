from django.conf import settings
from django.db import models
from course.models import Course


class Enrollment(models.Model):
    OPEN_DATE_FORMAT = "%Y-%m-%d %X"

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    course = models.ForeignKey(Course)
