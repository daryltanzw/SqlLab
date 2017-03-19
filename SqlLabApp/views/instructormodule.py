from SqlLabApp.forms.instructormodule import CreateModuleForm
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from SqlLabApp.models import Class, ClassTeacherTeaches

class CreateModuleFormView(FormView):
    form_class = CreateModuleForm
    template_name = 'SqlLabApp/instructormodule.html'
    success_url = '/'

    def get(self, request):
        create_module_form = CreateModuleForm
        class_list = ClassTeacherTeaches.objects.filter(teacher_email_id=request.user.email)
        class_names = []

        for module in class_list:
            class_names.append(Class.objects.get(classid=module.classid_id).class_name)

        return self.render_to_response(
            self.get_context_data(
                class_list=sorted(class_names),
                create_module_form=create_module_form,
            )
        )

    def post(self, request, *args, **kwargs):
        create_module_form = self.form_class(request.POST)
        if create_module_form.is_valid():
            create_module_form.save(request.user)
            return HttpResponseRedirect("../instructormodule")

        else:
            return self.render_to_response(
                self.get_context_data(
                    create_module_form=create_module_form,
                )
            )