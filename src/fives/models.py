from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.
class Five(models.Model):
	user_from = models.ForeignKey(settings.AUTH_USER_MODEL)
	user_to = models.ForeignKey(settings.AUTH_USER_MODEL)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, default=timezone.now())

	# def __unicode__(self):
	# 	return self.title[:10]
    #
	# class Meta:
	# 	ordering = ['-updated', '-timestamp']
