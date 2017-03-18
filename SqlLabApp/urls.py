from django.conf.urls import url
from django.contrib import admin
from SqlLabApp.views.login import LoginFormView, MainView, RegistrationFormView
from SqlLabApp.views.instructormodule import CreateModuleFormView
from SqlLabApp.views.instructortest import InstructorTestFormView
from SqlLabApp.views.createtest import CreateTestFormView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^register/$', RegistrationFormView.as_view(), name='register'),
    url(r'^instructormodule/$', CreateModuleFormView.as_view(), name='instructormodule'),
    url(r'^instructortest/$', InstructorTestFormView.as_view(), name='instructortest'),
    url(r'^createmodule/$', CreateModuleFormView.as_view(), name='createmodule'),
    url(r'^createtest/$', CreateTestFormView.as_view(), name='createtest'),
]
