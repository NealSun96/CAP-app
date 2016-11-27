from django.db import models
from course.models import Course
from employee_title.models import EmployeeTitle


class Assignment(models.Model):
    ordering = models.IntegerField()

    # ASSIGNMENT_TYPES = (
    #     ('feedback', 'Feedback'),
    #     ('action_plan', 'Behaviour Changing Action Plan'),
    #     ('knowledge_test', 'Knowledge Test'),
    #     ('self_diagnosis', 'Self-Diagnosis')
    # )
    # assignment_type = models.CharField(max_length=100, choices=ASSIGNMENT_TYPES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    level = models.CharField(max_length=100, choices=EmployeeTitle.ACCEPTED_NAMES)
    title = models.CharField(max_length=100)
    # open_date = models.DateTimeField()
    time_span = models.FloatField()
    total_score = models.IntegerField()

    class Meta:
        ordering = ['ordering']
