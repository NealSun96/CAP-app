from django.db import models
from assignment.models import Assignment


class KnowledgeTest(Assignment):
    time_span = models.FloatField()
