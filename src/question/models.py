from django.db import models


class Question(models.Model):
    question_body = models.TextField()
    answer_keys = models.TextField()
    right_answer = models.TextField(default="", null=True)
