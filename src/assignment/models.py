from datetime import datetime
from django.db import models
from course.models import Course
from employee_title.models import EmployeeTitle


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        abstract = True
