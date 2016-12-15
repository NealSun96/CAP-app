from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from action_plan_answer.models import ActionPlanAnswer


class ActionPlanAnswerResource(ModelResource):
    class Meta:
        queryset = ActionPlanAnswer.objects.all()
        fields = ["answers", "action_plan", "enrollment"]
        allowed_method = ['post']
        resource_name = 'feedback'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(ActionPlanAnswerResource, self).obj_create(bundle, **kwargs)
        if ActionPlanAnswer.objects.filter(enrollment=bundle.data.get('enrollment_id')).first():
            raise BadRequest('Action Plan answer already exists')
        bundle.obj.action_plan = bundle.obj.enrollment.course.actionplan_set.first()
        bundle.obj.save()
        return bundle
