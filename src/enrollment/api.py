# -*- coding: utf-8 -*-

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
from tastypie.utils import trailing_slash, dict_strip_unicode_keys

from .models import Enrollment
from feedback.models import Feedback
from action_plan_answer.models import ActionPlanAnswer
from knowledge_test.models import KnowledgeTest
from knowledge_test_answer.models import KnowledgeTestAnswer
from knowledge_test_first_score.models import KnowledgeTestFirstScore
from knowledge_test_start.models import KnowledgeTestStart
from diagnosis.models import Diagnosis
from djgap.corsresource import CorsResourceBase


class EnrollmentResource(CorsResourceBase, ModelResource):
    class Meta:
        queryset = Enrollment.objects.all()
        allowed_method = ['get']
        resource_name = 'enrollment'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/enrollments%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_enrollments'), name="api_get_enrollments"),
            url(r"^(?P<resource_name>%s)/assignments/(?P<id>\d+)/(?P<type>\w+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_assignments'), name="api_get_assignments"),
            url(r"^(?P<resource_name>%s)/upload/(?P<id>\d+)/(?P<type>\w+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('upload_answers'), name="api_upload_answers"),
            url(r"^(?P<resource_name>%s)/check_mark/(?P<id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('check_mark'), name="api_check_mark"),
            url(r"^(?P<resource_name>%s)/record_start/(?P<id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('record_start'), name="api_record_start"),
            url(r"^(?P<resource_name>%s)/first_score/(?P<id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('first_score'), name="api_first_score"),
        ]

    def get_enrollments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        # Do the query.
        enrollments = Enrollment.objects.filter(user=request.user).filter(course__done=False)
            #.filter(course__start_time=F('start_time'))

        objects = []

        for enrollment in enrollments:
            bundle = self.build_bundle(obj=enrollment, request=request)
            bundle.data['id'] = enrollment.id
            bundle.data['course_name'] = enrollment.course.course_name
            bundle.data['teacher_name'] = enrollment.course.teacher.get_full_name()
            if enrollment.course.picture:
                bundle.data['picture_path'] = enrollment.course.picture.url

            has_feedback = enrollment.feedback_set.count() > 0
            bundle.data['feedback_status'] = "已完成" if has_feedback else "未完成"
            bundle.data['feedback_color'] = "{color: 'green'}" if has_feedback else "{color: 'red'}"

            has_action_plan = enrollment.course.actionplan_set.count() > 0
            has_action_plan_answer = enrollment.actionplananswer_set.count() > 0
            bundle.data['action_plan_status'] = "已完成" if has_action_plan_answer else "未完成" \
                if has_action_plan else "未开放"
            bundle.data['action_plan_color'] = "{color: 'green'}" if has_action_plan_answer else "{color: 'red'}" \
                if has_action_plan else "{color: 'black'}"

            current_date = datetime.now(pytz.timezone('Asia/Shanghai'))
            knowledge_test_open_date = (enrollment.start_time
                                       + timedelta(enrollment.course.KNOWLEDGE_TEST_OPEN_DAYS)).\
                astimezone(pytz.timezone('Asia/Shanghai'))
            knowledge_test_open_string = knowledge_test_open_date.strftime(enrollment.OPEN_DATE_FORMAT)
            has_knowledge_test = enrollment.course.knowledgetest_set.count() > 0
            has_knowledge_test_answer = enrollment.knowledgetestanswer_set.count() > 0
            if has_knowledge_test_answer:
                bundle.data['knowledge_test_status'], bundle.data['knowledge_test_color'] = '已完成', "{color: 'green'}"
            elif not has_knowledge_test or not has_feedback or not has_action_plan_answer:
                bundle.data['knowledge_test_status'], bundle.data['knowledge_test_color'] = '未开放', "{color: 'black'}"
            elif current_date >= knowledge_test_open_date:
                bundle.data['knowledge_test_status'], bundle.data['knowledge_test_color'] = '未完成', "{color: 'red'}"
            else:
                bundle.data['knowledge_test_status'], bundle.data['knowledge_test_color'] = '开放于%s' % knowledge_test_open_string, "{color: 'black'}"

            diagnosis_open_date = (enrollment.start_time + timedelta(enrollment.course.DIAGNOSIS_OPEN_DAYS)).\
                astimezone(pytz.timezone('Asia/Shanghai'))
            diagnosis_open_string = diagnosis_open_date.strftime(enrollment.OPEN_DATE_FORMAT)
            has_diagnosis = enrollment.diagnosis_set.count() > 0
            if has_diagnosis:
                bundle.data['diagnosis_status'], bundle.data['diagnosis_color'] = '已完成', "{color: 'green'}"
            elif not has_feedback or not has_action_plan_answer:
                bundle.data['diagnosis_status'], bundle.data['diagnosis_color'] = '未开放', "{color: 'black'}"
            elif current_date >= diagnosis_open_date:
                bundle.data['diagnosis_status'], bundle.data['diagnosis_color'] = '未完成', "{color: 'red'}"
            else:
                bundle.data['diagnosis_status'], bundle.data['diagnosis_color'] = '开放于%s' % diagnosis_open_string, "{color: 'black'}"
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)

    def get_assignments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        try:
            enrollment = Enrollment.objects.get(id=kwargs['id'], user=request.user, course__done=False)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Enrollment does not exist'))

        a_type = kwargs['type']
        if a_type not in ['action_plan', 'knowledge_test', 'diagnosis']:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment type'))
        objects = []

        if a_type == 'action_plan':
            if enrollment.course.actionplan_set.count() <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Action plan does not exist'))

            if enrollment.actionplananswer_set.count() > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Action plan already submitted'))

            action_plan = enrollment.course.actionplan_set.first()
            bundle = self.build_bundle(obj=action_plan, request=request)
            # bundle.data['action_plan_id'] = action_plan.id
            bundle.data['action_points'] = json.loads(action_plan.action_points)
            objects.append(bundle)
        elif a_type == 'knowledge_test':
            if enrollment.course.knowledgetest_set.count() <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Knowledge test does not exist'))

            if enrollment.knowledgetestanswer_set.count() > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Knowledge test already submitted'))

            knowledge_test = enrollment.course.knowledgetest_set.first()
            bundle = self.build_bundle(obj=knowledge_test, request=request)
            # bundle.data['knowledge_test_id'] = knowledge_test.id
            bundle.data['questions'] = [{
                'question': question.question.question_body,
                'answer_keys': [answer for answer in json.loads(question.question.answer_keys)],
                'score': question.score
            } for question in knowledge_test.questionordered_set.all()]
            objects.append(bundle)
        else:
            if enrollment.actionplananswer_set.count() <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Diagnosis form does not exist'))

            if enrollment.diagnosis_set.count() > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Diagnosis already submitted'))

            diagnosis = enrollment.actionplananswer_set.first()
            bundle = self.build_bundle(obj=diagnosis, request=request)
            bundle.data['diagnosis_points'] = json.loads(diagnosis.answers)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)

    def upload_answers(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            enrollment = Enrollment.objects.get(id=kwargs['id'], user=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Enrollment does not exist'))

        a_type = kwargs['type']
        if a_type not in ['feedback', 'action_plan', 'knowledge_test', 'diagnosis']:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment type'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        if a_type == 'feedback':
            if enrollment.feedback_set.count() > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Feedback already exists'))
            Feedback(enrollment=enrollment, feedbacks=bundle.data.get('feedbacks')).save()
        elif a_type == 'action_plan':
            if enrollment.actionplananswer_set.count() > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Action plan answer already exists'))
            if enrollment.course.actionplan_set.count() <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Action plan does not exist'))
            action_plan = enrollment.course.actionplan_set.first()
            ActionPlanAnswer(enrollment=enrollment, action_plan=action_plan, answers=bundle.data.get('answers')).save()
        elif a_type == 'knowledge_test':
            if enrollment.knowledgetestanswer_set.count() > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Knowledge test answer already exists'))
            if enrollment.course.knowledgetest_set.count() <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Knowledge test does not exist'))
            knowledge_test = enrollment.course.knowledgetest_set.first()
            if enrollment.knowledgeteststart_set.count() <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Knowledge test start time does not exist'))
            if enrollment.knowledgetestfirstscore_set.count() <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Knowledge test first score does not exist'))

            time_now = datetime.now(pytz.timezone('Asia/Shanghai'))
            dtime = time_now - enrollment.knowledgeteststart_set.first().start_time
            KnowledgeTestAnswer(enrollment=enrollment, knowledge_test=knowledge_test, answers=bundle.data.get('answers'),
                                time_taken=dtime.seconds, first_score=enrollment.knowledgetestfirstscore_set.first().first_score,
                                final_score=bundle.data.get('final_score'), completion_date=time_now).save()
        elif a_type == 'diagnosis':
            if enrollment.diagnosis_set.count() > 0:
                raise ImmediateHttpResponse(HttpBadRequest('Diagnosis already exists'))
            if enrollment.actionplananswer_set.count() <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Diagnosis form does not exist'))
            Diagnosis(enrollment=enrollment, self_diagnosis=bundle.data.get('self_diagnosis'),
                      other_diagnosis=bundle.data.get('other_diagnosis'),
                      completion_date=datetime.now(pytz.timezone('Asia/Shanghai'))).save()

        return self.create_response(request, {})

    def check_mark(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            enrollment = Enrollment.objects.get(id=kwargs['id'], user=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Enrollment does not exist'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        answers = json.loads(bundle.data.get("answers"))
        if enrollment.course.knowledgetest_set.count() <= 0:
            raise ImmediateHttpResponse(HttpNotFound('Knowledge test does not exist'))
        knowledge_test = enrollment.course.knowledgetest_set.first()
        if not answers or answers and knowledge_test.questionordered_set.count() != len(answers):
            raise ImmediateHttpResponse(HttpBadRequest('Bad answers'))

        score = 0
        total_score = 0
        for question, answer in zip(knowledge_test.questionordered_set.all(), answers):
            score += question.score if question.question.right_answer == answer else 0
            total_score += question.score

        return self.create_response(request, {
            'objects': [score, total_score, KnowledgeTest.PASS_MARK]
        })

    def record_start(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            enrollment = Enrollment.objects.get(id=kwargs['id'], user=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Enrollment does not exist'))
        if enrollment.knowledgeteststart_set.count() <= 0:
            KnowledgeTestStart(enrollment=enrollment, start_time=datetime.now(pytz.timezone('Asia/Shanghai'))).save()
        else:
            kts = KnowledgeTestStart.objects.get(enrollment=enrollment)
            kts.start_time = datetime.now(pytz.timezone('Asia/Shanghai'))
            kts.save()

        return self.create_response(request, {})

    def first_score(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            enrollment = Enrollment.objects.get(id=kwargs['id'], user=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Enrollment does not exist'))
        if enrollment.knowledgetestfirstscore_set.count()> 0:
            return self.create_response(request, {})

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        KnowledgeTestFirstScore(enrollment=enrollment, first_score=bundle.data.get("first_score")).save()

        return self.create_response(request, {})
