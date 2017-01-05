from django.db import models
from django.contrib.auth.models import Group, Permission


class EmployeeTitle(models.Model):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    TITLE_TEACHER = 'teacher'
    TITLE_STUDENT_MANAGER = 'manager'
    TITLE_STUDENT_NON_MANAGER = 'non-manager'
    TITLE_UNKNOWN = 'unknown'

    TITLE_PERMS = {
        TITLE_TEACHER: ['Can add posting'],
        TITLE_STUDENT_MANAGER: [],
        TITLE_STUDENT_NON_MANAGER: [],
        TITLE_UNKNOWN: []
    }
    # a mapping from provided names to f1 app's group names
    ACCEPTED_NAMES = {
        "teacher": TITLE_TEACHER,
        "manager": TITLE_STUDENT_MANAGER,
        "non-manager": TITLE_STUDENT_NON_MANAGER,
    }

    ASSIGNMENT_LEVEL_CHOICES = (
        (TITLE_STUDENT_MANAGER, 'manager'),
        (TITLE_STUDENT_NON_MANAGER, 'non-manager'),
        ('discarded', 'DISCARDED')
    )

    @staticmethod
    def get_or_create_title_group(title):
        title = title if title in EmployeeTitle.TITLE_PERMS.keys() else EmployeeTitle.TITLE_UNKNOWN
        try:
            return Group.objects.get(name=title)
        except Group.DoesNotExist:
            group = Group.objects.create(name=title)
            for permission_name in EmployeeTitle.TITLE_PERMS[title]:
                group.permissions.add(Permission.objects.get(name=permission_name))
            group.save()
            return group
