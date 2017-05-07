# -*- coding: utf-8 -*-

import base64

from django.conf.urls import url
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash, dict_strip_unicode_keys

from employee_title.models import EmployeeTitle
from djgap.corsresource import CorsResourceBase


class EmployeeTitleResource(CorsResourceBase, ModelResource):
    class Meta:
        queryset = EmployeeTitle.objects.all()
        allowed_method = ['get']
        resource_name = 'employee_title'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add_titles%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('add_titles'), name="api_add_titles"),
            url(r"^(?P<resource_name>%s)/get_titles%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_titles'), name="api_get_titles"),
        ]

    def get_object_list(self, request):
        return EmployeeTitle.objects.none()

    def add_titles(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        if not request.user.is_superuser:
            raise ImmediateHttpResponse(HttpBadRequest('Not a superuser'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        file_data = bundle.data.get('file')
        if isinstance(file_data, basestring) and file_data.startswith('data:text'):
            _, str = file_data.split(';base64,')
            file_data = base64.b64decode(str)
        else:
            raise ImmediateHttpResponse(HttpBadRequest('该文件无法被阅读'))
        rows = file_data.split("\n")
        rows = [x for x in rows if x != ""]
        for row in rows:
            if EmployeeTitle.objects.filter(username=row, title=EmployeeTitle.TITLE_TEACHER).count() == 0:
                EmployeeTitle(username=row, title=EmployeeTitle.TITLE_TEACHER).save()
        object_list = {
            'objects': len(rows),
        }
        return self.create_response(request, object_list)

    def get_titles(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        if not request.user.is_superuser:
            raise ImmediateHttpResponse(HttpBadRequest('Not a superuser'))

        data = [e.username for e in EmployeeTitle.objects.filter(title=EmployeeTitle.TITLE_TEACHER).all()]
        data.sort()
        object_list = {
            'objects': data
        }
        return self.create_response(request, object_list)
