from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from SqlLabApp.views.login import LoginFormView, MainView, RegistrationFormView
from SqlLabApp.views.module import InstructorModuleFormView
from SqlLabApp.views.teacher_manage_module import TeacherManageModuleFormView
from SqlLabApp.views.test import InstructorTestFormView
from SqlLabApp.views.createmodule import CreateModuleFormView
from SqlLabApp.views.createtest import CreateTestFormView
from SqlLabApp.views.taketest import TakeTestFormView
from SqlLabApp.views.editmodule import EditModuleFormView
from SqlLabApp.views.deletemodule import DeleteModuleView
from SqlLabApp.views.edittest import EditTestFormView
from SqlLabApp.views.deletetest import DeleteTestView
from SqlLabApp.views.testattempt import TestAttemptFormView
from SqlLabApp.views.helpguide import HelpView
from SqlLabApp.jquerymethods import execute_query

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^register/$', RegistrationFormView.as_view(), name='register'),
    url(r'^module/$', InstructorModuleFormView.as_view(), name='module'),
    url(r'^createmodule/$', CreateModuleFormView.as_view(), name='createmodule'),
    url(r'^(?P<class_id>[\w\-]+)/test/$', InstructorTestFormView.as_view(), name='test'),
    url(r'^(?P<class_id>[\w\-]+)/createtest/$', CreateTestFormView.as_view(), name='createtest'),
    url(r'^(?P<test_id>[\w\-]+)/taketest/$', TakeTestFormView.as_view(), name='taketest'),
    url(r'^(?P<class_id>[\w\-]+)/editmodule/$', EditModuleFormView.as_view(), name='editmodule'),
    url(r'^(?P<class_id>[\w\-]+)/deletemodule/$', DeleteModuleView.as_view(), name='deletemodule'),
    url(r'^(?P<test_id>[\w\-]+)/edittest/$', EditTestFormView.as_view(), name='edittest'),
    url(r'^(?P<test_id>[\w\-]+)/deletetest/$', DeleteTestView.as_view(), name='deletetest'),
    url(r'^(?P<test_id>[\w\-]+)/testattempt/$', TestAttemptFormView.as_view(), name='testattempt'),
    url(r'^(?P<class_id>[\w\-]+)/teachermanagemodule/$', TeacherManageModuleFormView.as_view(), name='teachermanagemodule'),
    url(r'^help/$', HelpView.as_view(), name='help'),
    url(r'^(?P<test_id>[\w\-]+)/taketest/execute_query/', execute_query, name='executequery'),
]
