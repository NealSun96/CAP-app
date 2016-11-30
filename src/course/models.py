import os
from django.conf import settings
from django.db import models


def get_image_path(instance, filename):
    return os.path.join('course_photos', str(instance.id), filename)


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    done = models.BooleanField(default=False)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL)
    picture = models.ImageField(upload_to=get_image_path, blank=True, null=True)
