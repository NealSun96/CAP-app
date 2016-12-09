from datetime import datetime, timedelta

from django.conf.urls import url
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from .models import Enrollment
from feedback.models import Feedback


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
            url(r"^(?P<resource_name>%s)/assignments/(?P<id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_assignments'), name="api_get_assignments"),
        ]

    def get_enrollments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        # Do the query.
        enrollments = Enrollment.objects.filter(user=request.user).filter(course__done=False)

        objects = []

        for enrollment in enrollments:
            bundle = self.build_bundle(obj=enrollment, request=request)
            bundle.data['id'] = enrollment.id
            bundle.data['course_name'] = enrollment.course.course_name
            bundle.data['teacher_name'] = enrollment.course.teacher.get_full_name()
            if enrollment.course.picture:
                bundle.data['picture_path'] = enrollment.course.picture.url

            has_feedback = len(enrollment.feedback_set.all()) > 0
            bundle.data['feedback_status'] = "Completed" if has_feedback else "Available"

            user_group = request.user.groups.all()[0].name
            has_action_plan = len(enrollment.course.actionplan_set.filter(level=user_group).all()) > 0
            has_action_plan_answer = len(enrollment.actionplananswer_set.all()) > 0
            bundle.data['action_plan_status'] = "Completed" if has_action_plan_answer else "Available" \
                if has_action_plan else "Unavailable"
            knowledge_test_open = (enrollment.course.start_time
                                   + timedelta(enrollment.course.KNOWLEDGE_TEST_OPEN_DAYS))\
                .strftime(enrollment.OPEN_DATE_FORMAT)
            has_knowledge_test = len(enrollment.course.knowledgetest_set.filter(level=user_group).all()) > 0
            has_knowledge_test_answer = len(enrollment.knowledgetestanswer_set.all()) > 0
            bundle.data['knowledge_test_status'] = 'Completed' if has_knowledge_test_answer else \
                ('Open at %s' % knowledge_test_open) if has_knowledge_test else 'Unavailable'
            diagnosis_open = (enrollment.course.start_time + timedelta(enrollment.course.DIAGNOSIS_OPEN_DAYS)) \
                .strftime(enrollment.OPEN_DATE_FORMAT)
            has_diagnosis = len(enrollment.diagnosis_set.all()) > 0
            bundle.data['diagnosis_status'] = 'Completed' if has_diagnosis else 'Open at %s' % diagnosis_open \
                if has_action_plan_answer else 'Unavailable'
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)

    def get_assignments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        # Do the query.
        enrollments = Enrollment.objects.filter(id=kwargs['id'])
        enrollment = enrollments[0]
        objects = []

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
