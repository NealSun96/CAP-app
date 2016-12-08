from django.db import models
from answer.models import Answer


class Feedback(Answer):
    feedbacks = models.TextField()
