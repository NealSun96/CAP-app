# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from tastypie import http
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.exceptions import BadRequest, ImmediateHttpResponse

from employee_title.models import EmployeeTitle
from .corsresource import CorsResourceBase


class LoginResource(CorsResourceBase, ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ["first_name", "last_name", "username"]
        allowed_method = ['get']
        resource_name = 'login'
        authorization = DjangoAuthorization()
        authentication = BasicAuthentication()
        always_return_data = True

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(username=bundle.request.user.username)

    def dehydrate(self, bundle):
        username = bundle.data.get('username')
        user = User.objects.get(username=username)
        bundle.data['api_key'] = ApiKey.objects.get_or_create(user=user)[0].key
        return bundle

    def is_authenticated(self, request):
        ''' Overriding to delete www-authenticate, preventing browser popup '''
        auth_result = self._meta.authentication.is_authenticated(request)

        if isinstance(auth_result, HttpResponse):
            del auth_result['WWW-Authenticate']
            raise ImmediateHttpResponse(response=auth_result)

        if not auth_result is True:
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())


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
            raise BadRequest('该用户名已存在')
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
