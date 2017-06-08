import pytz
from datetime import datetime

from django.conf import settings
from django.db import models
from course.models import Course


class Enrollment(models.Model):
    OPEN_DATE_FORMAT = "%Y-%m-%d %X"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Shanghai')))
