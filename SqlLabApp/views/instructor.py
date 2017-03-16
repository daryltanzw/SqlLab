from django.views.generic import FormView

from SqlLabApp.forms.instructor import InstructorForm


class InstructorFormView(FormView):
    form_class = InstructorForm
    template_name = 'SqlLabApp/instructor.html'
    success_url = '/'
