from django.conf.urls import url
from django.contrib import admin
from SqlLabApp.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^register/$', RegistrationFormView.as_view(), name='register'),
    url(r'^instructor/$', InstructorFormView.as_view(), name='instructor'),
    url(r'^createtest/$', CreateTestFormView.as_view(), name='createtest'),
]
