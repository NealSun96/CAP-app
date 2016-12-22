from employee_title.models import EmployeeTitle
EmployeeTitle(username="test2", title="manager").save()
EmployeeTitle(username="teacher1", title="teacher").save()
from django.contrib.auth.models import User
User(first_name="tea", last_name="cher", username="teacher1", password="edpp").save()
User(first_name="test", last_name="person", username="test2", password="edpp").save()
teacher = User.objects.get(username="teacher1")
user = User.objects.get(username="test2")
import pytz
from datetime import datetime, timedelta
from course.models import Course
Course(course_name="course1", start_time=datetime.now(pytz.timezone('Asia/Shanghai')) - timedelta(35), teacher=teacher).save()
Course(course_name="course2", start_time=datetime.now(pytz.timezone('Asia/Shanghai')), teacher=teacher).save()
course1 = Course.objects.get(course_name='course1')
course2 = Course.objects.get(course_name='course2')
from enrollment.models import Enrollment
Enrollment(user=user, course=course1).save()
Enrollment(user=user, course=course2).save()
import json
from action_plan.models import ActionPlan
points = ['point1', 'point2', 'point3', 'point4']
ActionPlan(course=course1, level="manager", action_points=json.dumps(points)).save()
ActionPlan(course=course2, level="non-manager", action_points=json.dumps(points)).save()
from knowledge_test.models import KnowledgeTest
points = ['point1', 'point2', 'point3', 'point4']
KnowledgeTest(course=course1, level="manager", time_span=10).save()
KnowledgeTest(course=course2, level="manager", time_span=10).save()
test1 = course1.knowledgetest_set.first()
test2 = course2.knowledgetest_set.first()
from question.models import Question
options = ['option1', 'option2', 'option3', 'option4']
Question(question_body='questionA', answer_keys=json.dumps(options), right_answer="option2").save()
Question(question_body='questionB', answer_keys=json.dumps(options), right_answer="option3").save()
questionA = Question.objects.get(question_body='questionA')
questionB = Question.objects.get(question_body='questionB')
from question_ordered.models import QuestionOrdered
QuestionOrdered(ordering=0, test=test1, question=questionA, score=5).save()
QuestionOrdered(ordering=1, test=test2, question=questionA, score=3).save()
QuestionOrdered(ordering=1, test=test1, question=questionB, score=3).save()
QuestionOrdered(ordering=0, test=test2, question=questionB, score=5).save()
