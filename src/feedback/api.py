from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from feedback.models import Feedback


class FeedbackResource(ModelResource):
    class Meta:
        queryset = Feedback.objects.all()
        fields = ["feedbacks", "enrollment"]
        allowed_method = ['post']
        resource_name = 'feedback'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()
        # filtering = {
        #     "username": ALL
        # }

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(FeedbackResource, self).obj_create(bundle, **kwargs)
        if Feedback.objects.filter(enrollment=bundle.data.get('enrollment')).first():
            raise BadRequest('Feedback already exists')
        bundle.obj.save()
        return bundle
