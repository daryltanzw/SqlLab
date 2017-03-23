from django.views.generic import FormView
from SqlLabApp.forms.test import InstructorTestForm

from SqlLabApp.models import UserRole, Class, TestForClass

class InstructorTestFormView(FormView):
    model = Class
    form_class = InstructorTestForm
    template_name = 'SqlLabApp/test.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        classid = self.kwargs['class_id']
        module_name = Class.objects.get(classid=classid).class_name
        create_module_form = InstructorTestForm
        test_list = TestForClass.objects.filter(classid_id=classid).order_by('test_name')
        user_role = UserRole.objects.get(email_id=request.user.email).role

        return self.render_to_response(
            self.get_context_data(
                user_role=user_role,
                classid=classid,
                test_list=test_list,
                module_name=module_name,
                create_module_form=create_module_form,
            )
        )