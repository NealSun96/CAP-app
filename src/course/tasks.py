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
    title_context = "CAP任务提醒"
    email_context = "尊敬的{}:\n"\
                    "您好，\n" \
                    "您的课程：{} 已有任务开放。开放的任务是：{}，请及时完成！\n" \
                    "C3／能力加速营"

    for course in Course.objects.all():
        if course.done:
            continue

        enrollments = course.enrollment_set.all()

        for enrollment in enrollments:
            per_email_context = ""
            current_date = datetime.now(pytz.timezone('Asia/Shanghai'))

            knowledge_test_open_date = (enrollment.start_time
                                        + timedelta(enrollment.course.KNOWLEDGE_TEST_OPEN_DAYS))
            diagnosis_open_date = (enrollment.start_time + timedelta(enrollment.course.DIAGNOSIS_OPEN_DAYS))
            has_knowledge_test = enrollment.course.knowledgetest_set.count() > 0
            has_knowledge_test_answer = enrollment.knowledgetestanswer_set.count() > 0
            has_action_plan_answer = enrollment.actionplananswer_set.count() > 0
            has_diagnosis = enrollment.diagnosis_set.count() > 0

            if knowledge_test_open_date <= current_date < knowledge_test_open_date + timedelta(notification_day_count) and \
                has_knowledge_test and not has_knowledge_test_answer:
                per_email_context = email_context.format(enrollment.user.first_name + " " + enrollment.user.last_name,
                                                        course.course_name,
                                                        "Knowledge Test")

            if diagnosis_open_date <= current_date < diagnosis_open_date + timedelta(notification_day_count) and \
                    has_action_plan_answer and not has_diagnosis:
                per_email_context = email_context.format(enrollment.user.first_name + " " + enrollment.user.last_name,
                                                        course.course_name,
                                                        "Diagnosis")

            if per_email_context:
                email = EmailMessage(
                    title_context,
                    per_email_context,
                    None,
                    [enrollment.user.username]
                )
                email.send()
