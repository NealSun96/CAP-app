from django.conf.urls import url
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from .models import Course
from djgap.corsresource import CorsResourceBase


class CourseResource(CorsResourceBase, ModelResource):
    class Meta:
        queryset = Course.objects.all()
        allowed_method = ['get']
        resource_name = 'course'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/courses%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_courses'), name="api_get_courses"),
        ]

    def get_courses(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        # Do the query.
        courses = Course.objects.filter(teacher=request.user)

        objects = []

        for course in courses:
            bundle = self.build_bundle(obj=course, request=request)
            bundle.data['id'] = course.id
            bundle.data['course_name'] = course.course_name
            bundle.data['start_time'] = course.start_time
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)
