from django.db import models
from assignment.models import Assignment


class ActionPlan(Assignment):
    action_points = models.TextField()
