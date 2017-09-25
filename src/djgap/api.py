# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse
from tastypie import http
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie.utils import trailing_slash, dict_strip_unicode_keys

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

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/change_password%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('change_password'), name="api_change_password"),
        ]

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
        print auth_result
        if isinstance(auth_result, HttpResponse):
            del auth_result['WWW-Authenticate']
            raise ImmediateHttpResponse(response=auth_result)

        if not auth_result is True:
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())

    def change_password(self, request, **kwargs):
        print request
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        request.user.set_password(bundle.data.get('new_password'))
        request.user.save()

        return self.create_response(request, {})


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
        except IntegrityError:
            raise BadRequest('该Email已存在')
        et = EmployeeTitle.objects.filter(username=bundle.data.get('username')).first()
        if et and et.title == EmployeeTitle.TITLE_TEACHER:
            group = EmployeeTitle.get_or_create_title_group(EmployeeTitle.TITLE_TEACHER)
        else:
            group = EmployeeTitle.get_or_create_title_group(bundle.data.get('bu'))
        bundle.obj.groups.add(group)
        bundle.obj.save()
        return bundle
