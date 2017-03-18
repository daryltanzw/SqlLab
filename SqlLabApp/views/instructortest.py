from django.views.generic import FormView

from SqlLabApp.forms.instructortest import InstructorTestForm


class InstructorTestFormView(FormView):
    form_class = InstructorTestForm
    template_name = 'SqlLabApp/instructortest.html'
    success_url = '/'
