from django.conf.urls import url
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from .models import Enrollment

# User = get_user_model()


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
        ]

    def get_enrollments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        # Do the query.
        enrollments = Enrollment.objects.filter(user=request.user)

        objects = []

        for enrollment in enrollments:
            bundle = self.build_bundle(obj=enrollment, request=request)
            bundle.data['course_name'] = enrollment.course.course_name
            bundle.data['teacher_name'] = enrollment.course.teacher.get_full_name()
            if enrollment.course.picture:
                bundle.data['picture_path'] = enrollment.course.picture.url
            complete_count = request.user.answer_set.filter(enrollment=enrollment).count()
            bundle.data['complete_count'] = complete_count
            bundle.data['latest_assignment_name'] = enrollment.course.assignment_set.all()[complete_count].title
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)
