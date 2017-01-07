import csv
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
        ]

    def get_object_list(self, request):
        return EmployeeTitle.objects.none()

    def add_titles(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        user_group = request.user.groups.first().name
        if user_group != "teacher":
            raise ImmediateHttpResponse(HttpBadRequest('Not a teacher'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        file_data = bundle.data.get('file')
        if isinstance(file_data, basestring) and file_data.startswith('data:text'):
            _, str = file_data.split(';base64,')
            file_data = base64.b64decode(str)
        else:
            raise ImmediateHttpResponse(HttpBadRequest('Bad CSV file'))
        file_data = [row for row in file_data.split("\n") if row != ""]
        reader = csv.reader(file_data)
        for row in reader:
            if len(row) != 2:
                raise ImmediateHttpResponse(HttpBadRequest('The csv file is not formatted correctly on the following line: %s' % ",".join(row)))
            title = EmployeeTitle.ACCEPTED_NAMES.get(row[1])
            if not title:
                raise ImmediateHttpResponse(HttpBadRequest("Title '%s' is not accepted" % row[1]))
            for et in EmployeeTitle.objects.filter(username=row[0]).all():
                et.delete()
            EmployeeTitle(username=row[0], title=title).save()
        object_list = {
            'objects': len(file_data)
        }
        return self.create_response(request, object_list)
