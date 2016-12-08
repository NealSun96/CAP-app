from datetime import datetime
from django.db import models
from course.models import Course
from employee_title.models import EmployeeTitle


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    level = models.CharField(max_length=100, choices=EmployeeTitle.ACCEPTED_NAMES)
    open_date = models.DateTimeField(default=datetime.today())

    class Meta:
        abstract = True
