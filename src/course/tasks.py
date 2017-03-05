# -*- coding: utf-8 -*-
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

from models import Course
import pytz
from datetime import datetime, timedelta
from django.core.mail import EmailMessage


@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="task_check_assignment",
    ignore_result=True
)
def task_check_assignment():
    """
    Saves latest image from Flickr
    """
    notification_day_count = 1
    email_context = "{} 的最晚递交时间是 {}"

    for course in Course.objects.all():
        if course.done:
            continue

        enrollments = course.enrollment_set.filter(start_time=course.start_time)

        for enrollment in enrollments:
            current_date = datetime.now(pytz.timezone('Asia/Shanghai'))

            user_group = enrollment.user.groups.all()[0].name
            knowledge_test_open_date = (enrollment.start_time
                                        + timedelta(enrollment.course.KNOWLEDGE_TEST_OPEN_DAYS))
            diagnosis_open_date = (enrollment.start_time + timedelta(enrollment.course.DIAGNOSIS_OPEN_DAYS))
            has_knowledge_test = len(enrollment.course.knowledgetest_set.filter(level=user_group).all()) > 0
            has_knowledge_test_answer = len(enrollment.knowledgetestanswer_set.all()) > 0
            has_action_plan_answer = len(enrollment.actionplananswer_set.all()) > 0
            has_diagnosis = len(enrollment.diagnosis_set.all()) > 0

            if knowledge_test_open_date - timedelta(notification_day_count) <= current_date < knowledge_test_open_date and \
                has_knowledge_test and not has_knowledge_test_answer:
                email_context = email_context.format("知识评测", knowledge_test_open_date)

            if diagnosis_open_date - timedelta(notification_day_count) <= current_date < diagnosis_open_date and \
                    has_action_plan_answer and not has_diagnosis:
                email_context = email_context.format("自我诊断", diagnosis_open_date)

            if email_context:
                email = EmailMessage(
                    '作业提醒',
                    email_context,
                    None,
                    [enrollment.user.username]
                )
                email.send()
