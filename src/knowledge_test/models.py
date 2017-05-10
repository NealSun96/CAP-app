from django.db import models
from assignment.models import Assignment


class KnowledgeTest(Assignment):
    PASS_MARK = 0.8

    time_span = models.FloatField()
