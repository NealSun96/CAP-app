import json

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
            url(r"^(?P<resource_name>%s)/get_assignments/(?P<id>\d+)/(?P<type>\w+)/(?P<level>\w+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_assignments'), name="api_get_assignments"),
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
        course.save()

        return self.create_response(request, {})

    def get_assignments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
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
                raise ImmediateHttpResponse(HttpNotFound('Action plan does not exist'))

            action_plan = course.actionplan_set.filter(level=a_level).first()
            bundle = self.build_bundle(obj=action_plan, request=request)
            bundle.data['action_points'] = json.loads(action_plan.action_points)
            objects.append(bundle)
        elif a_type == 'knowledge_test':
            if len(course.knowledgetest_set.filter(level=a_level).all()) <= 0:
                raise ImmediateHttpResponse(HttpNotFound('Knowledge test does not exist'))

            knowledge_test = course.knowledgetest_set.filter(level=a_level).first()
            bundle = self.build_bundle(obj=knowledge_test, request=request)
            bundle.data['questions'] = [{
                'ordering': question.question.ordering,
                'question': question.question.question_body,
                'answer_keys': [answer for answer in json.loads(question.question.answer_keys)],
                'right_answer': question.question.right_answer,
                'score': question.score
            } for question in knowledge_test.questionordered_set.all()]
            objects.append(bundle)

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
        course.start_time=bundle.data.get('start_time')
        course.done = bundle.data.get('done')
        course.save()

        return self.create_response(request, {})
