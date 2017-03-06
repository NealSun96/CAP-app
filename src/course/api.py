import json
import base64
import pytz

from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.conf.urls import url
from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpNotFound
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash, dict_strip_unicode_keys

from .models import Course
from employee_title.models import EmployeeTitle
from enrollment.models import Enrollment
from action_plan.models import ActionPlan
from knowledge_test.models import KnowledgeTest
from question.models import Question
from question_ordered.models import QuestionOrdered
from djgap.corsresource import CorsResourceBase


class CourseResource(CorsResourceBase, ModelResource):
    class Meta:
        queryset = Course.objects.all()
        fields = ["id", "course_name", "start_time", "done"]
        allowed_method = ['get']
        resource_name = 'course'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add_course%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('add_course'), name="api_add_course"),
            url(r"^(?P<resource_name>%s)/edit_course/(?P<id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('edit_course'), name="api_edit_course"),
            url(r"^(?P<resource_name>%s)/get_assignments/(?P<id>\d+)/(?P<type>\w+)/(?P<level>[\w-]+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_assignments'), name="api_get_assignments"),
            url(r"^(?P<resource_name>%s)/edit_assignments/(?P<id>\d+)/(?P<type>\w+)/(?P<level>[\w-]+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('edit_assignments'), name="api_edit_assignments"),
            url(r"^(?P<resource_name>%s)/enroll_students/(?P<id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('enroll_students'), name="api_enroll_students"),
            url(r"^(?P<resource_name>%s)/get_enrolled/(?P<id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_enrolled'), name="api_get_enrolled"),
            url(r"^(?P<resource_name>%s)/get_data/(?P<id>\d+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_data'), name="api_get_data"),
        ]

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(teacher=bundle.request.user)

    def add_course(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        user_group = request.user.groups.first().name
        if user_group != "teacher":
            raise ImmediateHttpResponse(HttpBadRequest('Not a teacher'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        teacher = bundle.data.get('teacher')
        if bundle.data.get('teacher') != bundle.request.user.username:
            try:
                other_teacher = User.objects.get(username=bundle.data.get('teacher'))
                other_teacher_group = other_teacher.groups.first().name
                if other_teacher_group != "teacher":
                    raise ImmediateHttpResponse(HttpBadRequest('Assigned teacher is not a teacher'))
            except ObjectDoesNotExist:
                raise ImmediateHttpResponse(HttpNotFound('Assigned teacher does not exist'))
            teacher = other_teacher

        time = pytz.timezone('Asia/Shanghai').localize(bundle.data.get('start_time'))

        Course(course_name=bundle.data.get('course_name'), start_time=time, teacher=teacher).save()

        return self.create_response(request, {})

    def edit_course(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        user_group = request.user.groups.first().name
        if user_group != "teacher":
            raise ImmediateHttpResponse(HttpBadRequest('Not a teacher'))

        try:
            course = Course.objects.get(id=kwargs['id'], teacher=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Course does not exist'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        if bundle.data.get('teacher') != bundle.request.user.username:
            try:
                other_teacher = User.objects.get(username=bundle.data.get('teacher'))
                other_teacher_group = other_teacher.groups.first().name
                if other_teacher_group != "teacher":
                    raise ImmediateHttpResponse(HttpBadRequest('Assigned teacher is not a teacher'))
            except ObjectDoesNotExist:
                raise ImmediateHttpResponse(HttpNotFound('Assigned teacher does not exist'))
            course.teacher = other_teacher

        course.course_name = bundle.data.get('course_name')
        course.start_time = pytz.timezone('Asia/Shanghai').localize(bundle.data.get('start_time'))
        course.done = bundle.data.get('done')

        image_data = bundle.data.get('picture')
        if isinstance(image_data, basestring) and image_data.startswith('data:image'):
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            course.picture = ContentFile(base64.b64decode(imgstr), name=str(course.id) + '.' + ext)
        else:
            raise ImmediateHttpResponse(HttpBadRequest('Bad picture'))
        course.save()

        return self.create_response(request, {})

    def get_assignments(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        try:
            course = Course.objects.get(id=kwargs['id'], teacher=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Course does not exist'))

        accepted_levels = set(EmployeeTitle.TITLE_PERMS.keys()) - {EmployeeTitle.TITLE_TEACHER, EmployeeTitle.TITLE_UNKNOWN}
        a_level = kwargs['level']
        if a_level not in accepted_levels:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment level'))

        a_type = kwargs['type']
        if a_type not in ['action_plan', 'knowledge_test']:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment type'))

        objects = []
        if a_type == 'action_plan':
            if len(course.actionplan_set.filter(level=a_level).all()) <= 0:
                bundle = self.build_bundle(request=request)
            else:
                action_plan = course.actionplan_set.filter(level=a_level).first()
                bundle = self.build_bundle(obj=action_plan, request=request)
                bundle.data['action_points'] = json.loads(action_plan.action_points)
            objects.append(bundle)
        elif a_type == 'knowledge_test':
            if len(course.knowledgetest_set.filter(level=a_level).all()) <= 0:
                bundle = self.build_bundle(request=request)
            else:
                knowledge_test = course.knowledgetest_set.filter(level=a_level).first()
                bundle = self.build_bundle(obj=knowledge_test, request=request)
                bundle.data['questions'] = [{
                    'ordering': question.ordering,
                    'question': question.question.question_body,
                    'answer_keys': [answer for answer in json.loads(question.question.answer_keys)],
                    'right_answer': question.question.right_answer,
                    'score': question.score
                } for question in knowledge_test.questionordered_set.all()]
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)

    def edit_assignments(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        user_group = request.user.groups.first().name
        if user_group != "teacher":
            raise ImmediateHttpResponse(HttpBadRequest('Not a teacher'))

        try:
            course = Course.objects.get(id=kwargs['id'], teacher=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Course does not exist'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        accepted_levels = set(EmployeeTitle.TITLE_PERMS.keys()) - {EmployeeTitle.TITLE_TEACHER, EmployeeTitle.TITLE_UNKNOWN}
        a_level = kwargs['level']
        if a_level not in accepted_levels:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment level'))

        a_type = kwargs['type']
        if a_type not in ['action_plan', 'knowledge_test']:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong assignment type'))

        if a_type == 'action_plan':
            if len(bundle.data.get('action_points')) != len(set(bundle.data.get('action_points'))):
                raise ImmediateHttpResponse(HttpBadRequest('Duplicate action points'))
            try:
                action_plan = ActionPlan.objects.get(course=course, level=a_level)
                action_plan.action_points = bundle.data.get('action_points')
                action_plan.save()
            except ActionPlan.DoesNotExist:
                ActionPlan(course=course, level=a_level, action_points=bundle.data.get('action_points')).save()
        elif a_type == 'knowledge_test':
            try:
                knowledge_test = KnowledgeTest.objects.get(course=course, level=a_level)
            except KnowledgeTest.DoesNotExist:
                knowledge_test = KnowledgeTest(course=course, level=a_level, time_span=0)
                knowledge_test.save()
            post_questions = json.loads(bundle.data.get('questions'))
            questions = knowledge_test.questionordered_set.all()
            for q, post_q in zip(questions, post_questions):
                q.score = post_q.get('score')
                q.question.question_body = post_q.get('question_body')
                answer_keys = post_q.get('answer_keys')
                if len(answer_keys) != len(set(answer_keys)):
                    raise ImmediateHttpResponse(HttpBadRequest('Duplicate answer keys in %s' % post_q.get('question_body')))
                q.question.answer_keys = json.dumps(answer_keys)
                q.question.right_answer = post_q.get('right_answer')
                q.question.save()
                q.save()
            ordering = len(questions)
            for post_q in post_questions[len(questions):]:
                answer_keys = post_q.get('answer_keys')
                if len(answer_keys) != len(set(answer_keys)):
                    raise ImmediateHttpResponse(HttpBadRequest('Duplicate answer keys in %s' % post_q.get('question_body')))
                new_question = Question(question_body=post_q.get('question_body'),
                                        answer_keys=json.dumps(answer_keys),
                                        right_answer=post_q.get('right_answer'))
                new_question.save()
                new_question_ordered = QuestionOrdered(ordering=ordering, test=knowledge_test,
                                                       question=new_question, score=post_q.get('score'))
                new_question_ordered.save()
                ordering += 1
            for q in questions[len(post_questions):]:
                q.delete()
                q.question.delete()

        return self.create_response(request, {})

    def enroll_students(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        user_group = request.user.groups.first().name
        if user_group != "teacher":
            raise ImmediateHttpResponse(HttpBadRequest('Not a teacher'))

        try:
            course = Course.objects.get(id=kwargs['id'], teacher=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Course does not exist'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        file_data = bundle.data.get('file')
        if isinstance(file_data, basestring) and file_data.startswith('data:text'):
            _, str = file_data.split(';base64,')
            file_data = base64.b64decode(str)
        else:
            raise ImmediateHttpResponse(HttpBadRequest('Bad file'))
        rows = file_data.split("\n")
        rows = [x for x in rows if x != ""]
        for row in rows:
            try:
                user = User.objects.get(username=row)
            except User.DoesNotExist:
                raise ImmediateHttpResponse(HttpBadRequest('Username %s does not exist' % row))
            for e in Enrollment.objects.filter(user=user).filter(course=course).all():
                e.delete()
            Enrollment(user=user, course=course, start_time=course.start_time).save()
        object_list = {
            'objects': len(rows),
        }
        return self.create_response(request, object_list)

    def get_enrolled(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        try:
            course = Course.objects.get(id=kwargs['id'], teacher=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Course does not exist'))

        context = "\n".join(enroll.user.username for enroll in course.enrollment_set.all())

        object_list = {
            'objects': context
        }
        return self.create_response(request, object_list)

    def get_data(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            course = Course.objects.get(id=kwargs['id'], teacher=request.user)
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(HttpNotFound('Course does not exist'))

        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        start_time = pytz.timezone('Asia/Shanghai').localize(bundle.data.get('start_time'))
        end_time = pytz.timezone('Asia/Shanghai').localize(bundle.data.get('end_time'))

        enrollments = course.enrollment_set.filter(start_time__gte=start_time)\
            .filter(start_time__lte=end_time)

        # KT average, KT completion days, KT time, D self improved rate, D completion days, D both improved rate
        data_dict = {
            "All": self.calc_data(enrollments)
        }
        for title in EmployeeTitle.TITLE_PERMS.keys():
            if title not in [EmployeeTitle.TITLE_TEACHER, EmployeeTitle.TITLE_UNKNOWN]:
                data_dict[title] = self.calc_data(enrollments.filter(user__groups__name=title))

        object_list = {
            'objects': data_dict
        }
        return self.create_response(request, object_list)

    def calc_data(self, querys):
        kt_total_first_score, kt_total_days, kt_total_time, kt_count = 0, 0, 0, 0.0
        d_self_improve, d_total_days, d_all_improve, d_count = 0, 0, 0, 0.0

        for enroll in querys:
            start_date = enroll.start_time

            if enroll.knowledgetestanswer_set.all() and enroll.knowledgetestfirstscore_set.all() and enroll.knowledgeteststart_set.all():
                kt_total_first_score += enroll.knowledgetestfirstscore_set.first().first_score
                kt_total_days += (enroll.knowledgetestanswer_set.first().completion_date - start_date).days
                kt_total_time += enroll.knowledgetestanswer_set.first().time_taken
                kt_count += 1

            if enroll.diagnosis_set.all():
                self_diagnosis = json.loads(enroll.diagnosis_set.first().self_diagnosis)
                other_diagnosis = json.loads(enroll.diagnosis_set.first().other_diagnosis)
                d_self_improve += 1 if 3 in self_diagnosis else 0
                d_total_days += (enroll.diagnosis_set.first().completion_date - start_date).days
                d_all_improve += 1 if (3, 3) in zip(self_diagnosis, other_diagnosis) else 0
                d_count += 1

        return [x / kt_count if kt_count > 0 else "N/A" for x in [kt_total_first_score, kt_total_days, kt_total_time]]\
               + [x / d_count if d_count > 0 else "N/A" for x in [d_self_improve, d_total_days, d_all_improve]]
