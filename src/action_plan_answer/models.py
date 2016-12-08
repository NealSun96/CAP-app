from django.db import models
from answer.models import Answer
from action_plan.models import ActionPlan


class ActionPlanAnswer(Answer):
    action_plan = models.ForeignKey(ActionPlan)
    answers = models.TextField()
