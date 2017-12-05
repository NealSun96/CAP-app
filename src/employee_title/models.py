from django.db import models
from django.contrib.auth.models import Group, Permission


class EmployeeTitle(models.Model):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    TITLE_TEACHER = 'teacher'
    TITLE_OTHERS = 'Others'

    TITLES = ["Cardio", "ENDO", "PION", "CRM", "EP", "Urology",
              "Structural Heart", "HK&TW", "Emerging Marketing",
              TITLE_OTHERS]

    @staticmethod
    def get_or_create_title_group(title):
        title = title if title in EmployeeTitle.TITLES + [EmployeeTitle.TITLE_TEACHER] else EmployeeTitle.TITLE_OTHERS
        try:
            return Group.objects.get(name=title)
        except Group.DoesNotExist:
            group = Group.objects.create(name=title)
            group.save()
            return group
