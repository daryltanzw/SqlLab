from django.views.generic import FormView
from SqlLabApp.forms.instructortest import InstructorTestForm

from SqlLabApp.models import Class, TestForClass

class InstructorTestFormView(FormView):
    model = Class
    form_class = InstructorTestForm
    template_name = 'SqlLabApp/instructortest.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        create_module_form = InstructorTestForm
        test_list = TestForClass.objects.filter(classid_id=self.kwargs['pk'])

        return self.render_to_response(
            self.get_context_data(
                test_list=test_list,
                create_module_form=create_module_form,
            )
        )