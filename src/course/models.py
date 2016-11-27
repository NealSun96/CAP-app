from django.db import models


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    # done = models.BooleanField(default=False)
