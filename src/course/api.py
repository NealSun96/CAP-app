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
        course.start_time=bundle.data.get('start_time')
        course.done = bundle.data.get('done')
        course.save()

        return self.create_response(request, {})
