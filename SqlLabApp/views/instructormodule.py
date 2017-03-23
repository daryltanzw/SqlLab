import operator

from SqlLabApp.forms.instructormodule import InstructorModuleForm
from django.views.generic import FormView
from SqlLabApp.models import Class, ClassTeacherTeaches


class InstructorModuleFormView(FormView):
    form_class = InstructorModuleForm
    template_name = 'SqlLabApp/instructormodule.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        create_module_form = InstructorModuleForm
        class_list = ClassTeacherTeaches.objects.filter(teacher_email_id=request.user.email)
        class_names = []

        for module in class_list:
            class_names.append(Class.objects.get(classid=module.classid_id))

        class_names.sort(key=operator.attrgetter('class_name'))

        return self.render_to_response(
            self.get_context_data(
                class_list=class_names,
                create_module_form=create_module_form,
            )
        )
