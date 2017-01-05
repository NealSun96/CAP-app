import json
import base64

from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.conf.urls import url
from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpNotFound
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash, dict_strip_unicode_keys

from .models import Course
from employee_title.models import EmployeeTitle
from action_plan.models import ActionPlan
from knowledge_test.models import KnowledgeTest
from question.models import Question
from question_ordered.models import QuestionOrdered
from djgap.corsresource import CorsResourceBase


class CourseResource(CorsResourceBase, ModelResource):
    class Meta:
        queryset = Course.objects.all()
        fields = ["id", "course_name", "start_time"]
        allowed_method = ['get']
        resource_name = 'course'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add_course%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('add_course'), name="api_add_course"),
            url(r"^(?P<resource_name>%s)/edit_course/(?P<id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('edit_course'), name="api_edit_course"),
            url(r"^(?P<resource_name>%s)/get_assignments/(?P<id>\d+)/(?P<type>\w+)/(?P<level>[\w-]+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_assignments'), name="api_get_assignments"),
            url(r"^(?P<resource_name>%s)/edit_assignments/(?P<id>\d+)/(?P<type>\w+)/(?P<level>[\w-]+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('edit_assignments'), name="api_edit_assignments"),
        ]

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(teacher=bundle.request.user)

    def add_course(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        user_group = request.user.groups.first().name
        if user_group != "teacher":
            raise ImmediateHttpResponse(HttpBadRequest('Not a teacher'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        Course(course_name=bundle.data.get('course_name'), start_time=bundle.data.get('start_time'), teacher=bundle.request.user).save()

        return self.create_response(request, {})

    def edit_course(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        user_group = request.user.groups.first().name
        if user_group != "teacher":
            raise ImmediateHttpResponse(HttpBadRequest('Not a teacher'))

        try:
            course = Course.objects.get(id=kwargs['id'], teacher=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Course does not exist'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        if bundle.data.get('teacher') != bundle.request.user.username:
            try:
                other_teacher = User.objects.get(username=bundle.data.get('teacher'))
                other_teacher_group = other_teacher.groups.first().name
                if other_teacher_group != "teacher":
                    raise ImmediateHttpResponse(HttpBadRequest('Assigned teacher is not a teacher'))
            except ObjectDoesNotExist:
                raise ImmediateHttpResponse(HttpNotFound('Assigned teacher does not exist'))
            course.teacher = other_teacher

        course.course_name = bundle.data.get('course_name')
        course.start_time = bundle.data.get('start_time')
        course.done = bundle.data.get('done')

        image_data = bundle.data.get('picture')
        if isinstance(image_data, basestring) and image_data.startswith('data:image'):
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            course.picture = ContentFile(base64.b64decode(imgstr), name=str(course.id) + '.' + ext)
        course.save()

        return self.create_response(request, {})

    def get_assignments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        try:
            course = Course.objects.get(id=kwargs['id'], teacher=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Course does not exist'))

        accepted_levels = set(EmployeeTitle.TITLE_PERMS.keys()) - {EmployeeTitle.TITLE_TEACHER, EmployeeTitle.TITLE_UNKNOWN}
        a_level = kwargs['level']
        if a_level not in accepted_levels:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment level'))

        a_type = kwargs['type']
        if a_type not in ['action_plan', 'knowledge_test']:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment type'))

        objects = []
        if a_type == 'action_plan':
            if len(course.actionplan_set.filter(level=a_level).all()) <= 0:
                bundle = self.build_bundle(request=request)
            else:
                action_plan = course.actionplan_set.filter(level=a_level).first()
                bundle = self.build_bundle(obj=action_plan, request=request)
                bundle.data['action_points'] = json.loads(action_plan.action_points)
            objects.append(bundle)
        elif a_type == 'knowledge_test':
            if len(course.knowledgetest_set.filter(level=a_level).all()) <= 0:
                bundle = self.build_bundle(request=request)
            else:
                knowledge_test = course.knowledgetest_set.filter(level=a_level).first()
                bundle = self.build_bundle(obj=knowledge_test, request=request)
                bundle.data['questions'] = [{
                    'ordering': question.ordering,
                    'question': question.question.question_body,
                    'answer_keys': [answer for answer in json.loads(question.question.answer_keys)],
                    'right_answer': question.question.right_answer,
                    'score': question.score
                } for question in knowledge_test.questionordered_set.all()]
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)

    def edit_assignments(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        user_group = request.user.groups.first().name
        if user_group != "teacher":
            raise ImmediateHttpResponse(HttpBadRequest('Not a teacher'))

        try:
            course = Course.objects.get(id=kwargs['id'], teacher=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Course does not exist'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        accepted_levels = set(EmployeeTitle.TITLE_PERMS.keys()) - {EmployeeTitle.TITLE_TEACHER, EmployeeTitle.TITLE_UNKNOWN}
        a_level = kwargs['level']
        if a_level not in accepted_levels:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment level'))

        a_type = kwargs['type']
        if a_type not in ['action_plan', 'knowledge_test']:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment type'))

        if a_type == 'action_plan':
            if len(bundle.data.get('action_points')) != len(set(bundle.data.get('action_points'))):
                raise ImmediateHttpResponse(HttpBadRequest('Duplicate action points'))
            try:
                action_plan = ActionPlan.objects.get(course=course, level=a_level)
                action_plan.action_points = bundle.data.get('action_points')
                action_plan.save()
            except ActionPlan.DoesNotExist:
                ActionPlan(course=course, level=a_level, action_points=bundle.data.get('action_points')).save()
        elif a_type == 'knowledge_test':
            try:
                knowledge_test = KnowledgeTest.objects.get(course=course, level=a_level)
            except KnowledgeTest.DoesNotExist:
                knowledge_test = KnowledgeTest(course=course, level=a_level, time_span=0)
                knowledge_test.save()
            post_questions = json.loads(bundle.data.get('questions'))
            questions = knowledge_test.questionordered_set.all()
            for q, post_q in zip(questions, post_questions):
                q.score = post_q.get('score')
                q.question.question_body = post_q.get('question_body')
                answer_keys = post_q.get('answer_keys')
                if len(answer_keys) != len(set(answer_keys)):
                    raise ImmediateHttpResponse(HttpBadRequest('Duplicate answer keys in %s' % post_q.get('question_body')))
                q.question.answer_keys = json.dumps(answer_keys)
                q.question.right_answer = post_q.get('right_answer')
                q.question.save()
                q.save()
            ordering = len(questions)
            for post_q in post_questions[len(questions):]:
                answer_keys = post_q.get('answer_keys')
                if len(answer_keys) != len(set(answer_keys)):
                    raise ImmediateHttpResponse(HttpBadRequest('Duplicate answer keys in %s' % post_q.get('question_body')))
                new_question = Question(question_body=post_q.get('question_body'),
                                        answer_keys=json.dumps(answer_keys),
                                        right_answer=post_q.get('right_answer'))
                new_question.save()
                new_question_ordered = QuestionOrdered(ordering=ordering, test=knowledge_test,
                                                       question=new_question, score=post_q.get('score'))
                new_question_ordered.save()
                ordering += 1
            for q in questions[len(post_questions):]:
                q.delete()
                q.question.delete()

        return self.create_response(request, {})
