# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.constants import ALL
from tastypie.models import ApiKey
from tastypie.resources import ModelResource

from employee_title.models import EmployeeTitle
from .corsresource import CorsResourceBase

# User = get_user_model()


class LoginResource(CorsResourceBase, ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ["first_name", "last_name", "username"]
        allowed_method = ['get']
        resource_name = 'login'
        authorization = DjangoAuthorization()
        authentication = BasicAuthentication()
        filtering = {
            "username": ALL
        }

    def dehydrate(self, bundle):
        username = bundle.data.get('username')
        user = User.objects.get(username=username)
        #instance, created = ApiKey.objects.get_or_create(user=user)
        bundle.data['api_key'] = ApiKey.objects.get_or_create(user=user)[0].key
        print bundle.data['api_key']
        return bundle


class RegisterResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ["username"]
        allowed_method = ['post']
        resource_name = 'register'
        authorization = Authorization()
        authentication = Authentication()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(RegisterResource, self).obj_create(bundle, **kwargs)
        # if bundle.data.get('username') == 'test_teacher':
        #     EmployeeTitle.objects.create(username='test_teacher', title='teacher')
        # else:
        #     EmployeeTitle.objects.create(username=bundle.data.get('username'), title='manager')
        bundle.obj.set_password(bundle.data.get('password'))
        bundle.obj.save()
        RegisterResource.assign_to_group(bundle.obj)
        return bundle

    @staticmethod
    def assign_to_group(user):
        try:
            employee_title = EmployeeTitle.objects.get(username=user.username)
            group = EmployeeTitle.get_or_create_title_group(employee_title.title)
        except EmployeeTitle.DoesNotExist:
            group = EmployeeTitle.get_or_create_title_group(EmployeeTitle.TITLE_UNKNOWN)

        user.groups.add(group)
        user.save()
