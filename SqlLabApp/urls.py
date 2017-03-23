from django.conf.urls import url
from django.contrib import admin
from SqlLabApp.views.login import LoginFormView, MainView, RegistrationFormView
from SqlLabApp.views.module import InstructorModuleFormView
from SqlLabApp.views.test import InstructorTestFormView
from SqlLabApp.views.createmodule import CreateModuleFormView
from SqlLabApp.views.createtest import CreateTestFormView
from SqlLabApp.views.taketest import TakeTestFormView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^register/$', RegistrationFormView.as_view(), name='register'),
    url(r'^module/$', InstructorModuleFormView.as_view(), name='module'),
    url(r'^createmodule/$', CreateModuleFormView.as_view(), name='createmodule'),
    url(r'^(?P<class_id>[0-9]+)/test/$', InstructorTestFormView.as_view(), name='test'),
    url(r'^(?P<class_id>[0-9]+)/createtest/$', CreateTestFormView.as_view(), name='createtest'),
    url(r'^(?P<test_id>[0-9]+)/taketest/$', TakeTestFormView.as_view(), name='taketest'),
]
