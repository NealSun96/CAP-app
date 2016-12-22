# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import IntegrityError
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.exceptions import BadRequest

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
        always_return_data = True
        # filtering = {
        #     "username": ALL
        # }

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(username=bundle.request.user.username)

    def dehydrate(self, bundle):
        username = bundle.data.get('username')
        user = User.objects.get(username=username)
        # instance, created = ApiKey.objects.get_or_create(user=user)
        bundle.data['api_key'] = ApiKey.objects.get_or_create(user=user)[0].key
        return bundle


class RegisterResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ["username", "first_name", "last_name"]
        allowed_method = ['post']
        resource_name = 'register'
        authorization = Authorization()
        authentication = Authentication()

    def get_object_list(self, request):
        return User.objects.none()

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(RegisterResource, self).obj_create(bundle, **kwargs)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()
            RegisterResource.assign_to_group(bundle.obj)
        except IntegrityError:
            raise BadRequest('That username already exists')
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
