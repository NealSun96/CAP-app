# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf.urls import url
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.models import ApiKey
from tastypie.resources import ModelResource

from employee_title.models import EmployeeTitle
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
            url(r"^(?P<resource_name>%s)/enrollments%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_children'), name="api_get_children"),
        ]


    # def get_list(self, request, **kwargs):
    #     request.user