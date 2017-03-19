from django.conf.urls import url
from django.contrib import admin
from SqlLabApp.views.login import LoginFormView, MainView, RegistrationFormView
from SqlLabApp.views.instructormodule import CreateModuleFormView
from SqlLabApp.views.instructortest import CreateTestFormView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^register/$', RegistrationFormView.as_view(), name='register'),
    url(r'^instructormodule/$', CreateModuleFormView.as_view(), name='instructormodule'),
    url(r'^(?P<pk>[0-9]+)/$', CreateTestFormView.as_view(), name='instructortest'),
]
