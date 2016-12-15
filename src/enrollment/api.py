import json
import pytz
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.conf.urls import url
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound, HttpBadRequest
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from .models import Enrollment


class EnrollmentResource(ModelResource):
    class Meta:
        queryset = Enrollment.objects.all()
        allowed_method = ['get']
        resource_name = 'enrollment'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()
        # filtering = {
        #     "username": ALL
        # }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/enrollments%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_enrollments'), name="api_get_enrollments"),
            url(r"^(?P<resource_name>%s)/assignments/(?P<id>\d+)/(?P<type>\w+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_assignments'), name="api_get_assignments"),
        ]

    def get_enrollments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        # Do the query.
        enrollments = Enrollment.objects.filter(user=request.user).filter(course__done=False)

        objects = []

        for enrollment in enrollments:
            bundle = self.build_bundle(obj=enrollment, request=request)
            bundle.data['id'] = enrollment.id
            bundle.data['course_name'] = enrollment.course.course_name
            bundle.data['teacher_name'] = enrollment.course.teacher.get_full_name()
            if enrollment.course.picture:
                bundle.data['picture_path'] = enrollment.course.picture.url

            has_feedback = len(enrollment.feedback_set.all()) > 0
            bundle.data['feedback_status'] = "Completed" if has_feedback else "Available"
            bundle.data['feedback_color'] = "{color: 'green'}" if has_feedback else "{color: 'red'}"

            user_group = request.user.groups.all()[0].name
            has_action_plan = len(enrollment.course.actionplan_set.filter(level=user_group).all()) > 0
            has_action_plan_answer = len(enrollment.actionplananswer_set.all()) > 0
            bundle.data['action_plan_status'] = "Completed" if has_action_plan_answer else "Available" \
                if has_action_plan else "Unavailable"
            bundle.data['action_plan_color'] = "{color: 'green'}" if has_action_plan_answer else "{color: 'red'}" \
                if has_action_plan else "{color: 'black'}"

            current_date = datetime.now(pytz.timezone('Asia/Shanghai'))
            knowledge_test_open_date = (enrollment.course.start_time
                                       + timedelta(enrollment.course.KNOWLEDGE_TEST_OPEN_DAYS))
            knowledge_test_open_string = knowledge_test_open_date.strftime(enrollment.OPEN_DATE_FORMAT)
            has_knowledge_test = len(enrollment.course.knowledgetest_set.filter(level=user_group).all()) > 0
            has_knowledge_test_answer = len(enrollment.knowledgetestanswer_set.all()) > 0
            bundle.data['knowledge_test_status'] = 'Completed' if has_knowledge_test_answer else \
                'Available' if has_knowledge_test and current_date >= knowledge_test_open_date else \
                ('Open at %s' % knowledge_test_open_string) if has_knowledge_test else 'Unavailable'
            bundle.data['knowledge_test_color'] = "{color: 'green'}" if has_knowledge_test_answer else \
                "{color: 'red'}" if has_knowledge_test and current_date >= knowledge_test_open_date else \
                "{color: 'black'}"

            diagnosis_open_date = (enrollment.course.start_time + timedelta(enrollment.course.DIAGNOSIS_OPEN_DAYS))
            diagnosis_open_string = diagnosis_open_date.strftime(enrollment.OPEN_DATE_FORMAT)
            has_diagnosis = len(enrollment.diagnosis_set.all()) > 0
            bundle.data['diagnosis_status'] = 'Completed' if has_diagnosis else \
                'Available' if has_action_plan_answer and current_date >= diagnosis_open_date else \
                'Open at %s' % diagnosis_open_string if has_action_plan_answer else 'Unavailable'
            bundle.data['diagnosis_color'] = "{color: 'green'}" if has_diagnosis else \
                "{color: 'red'}" if has_action_plan_answer and current_date >= diagnosis_open_date else \
                "{color: 'black'}"
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)

    def get_assignments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        try:
            enrollment = Enrollment.objects.get(id=kwargs['id'])
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Enrollment does not exist'))

        a_type = kwargs['type']
        if a_type not in ['action_plan', 'knowledge_test', 'diagnosis']:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment type'))
        objects = []

        user_group = request.user.groups.all()[0].name
        if a_type == 'action_plan':
            if len(enrollment.course.actionplan_set.filter(level=user_group).all()) <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Action plan does not exist'))

            if len(enrollment.actionplananswer_set.all()) > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Action plan already submitted'))

            action_plan = enrollment.course.actionplan_set.filter(level=user_group).all()[0]
            bundle = self.build_bundle(obj=action_plan, request=request)
            # bundle.data['action_plan_id'] = action_plan.id
            print action_plan.action_points
            bundle.data['action_points'] = json.loads(action_plan.action_points)
            objects.append(bundle)
        elif a_type == 'knowledge_test':
            if len(enrollment.course.knowledgetest_set.filter(level=user_group).all()) <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Knowledge test does not exist'))

            if len(enrollment.knowledgetestanswer_set.all()) > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Knowledge test already submitted'))

            knowledge_test = enrollment.course.knowledgetest_set.filter(level=user_group).all()[0]
            bundle = self.build_bundle(obj=knowledge_test, request=request)
            # bundle.data['knowledge_test_id'] = knowledge_test.id
            bundle.data['questions'] = [{
                'question': question.question.question_body,
                'answer_keys': [answer for answer in json.loads(question.question.answer_keys)],
                'score': question.score
            } for question in knowledge_test.questionordered_set.all()]
            bundle.data['timespan'] = knowledge_test.time_span
            objects.append(bundle)
        else:
            if len(enrollment.actionplananswer_set.all()) <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Diagnosis does not exist'))

            if len(enrollment.diagnosis_set.all()) > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Diagnosis already submitted'))

            diagnosis = enrollment.actionplananswer_set.all()[0]
            bundle = self.build_bundle(obj=diagnosis, request=request)
            bundle.data['diagnosis_points'] = json.loads(diagnosis.answers)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)
