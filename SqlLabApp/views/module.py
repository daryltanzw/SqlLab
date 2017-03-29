import operator

from SqlLabApp.forms.module import InstructorModuleForm
from django.views.generic import FormView
from SqlLabApp.models import UserRole, Class, ClassTeacherTeaches
from SqlLabApp.utils.CryptoSign import encryptData


class InstructorModuleFormView(FormView):
    form_class = InstructorModuleForm
    template_name = 'SqlLabApp/module.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        create_module_form = InstructorModuleForm
        class_list = ClassTeacherTeaches.objects.filter(teacher_email_id=request.user.email)
        class_names = []

        for module in class_list:
            class_names.append(Class.objects.get(classid=module.classid_id))

        for cobj in class_names:
            cobj.classid = encryptData(cobj.classid)

        class_names.sort(key=operator.attrgetter('class_name'))
        user_role = UserRole.objects.get(email_id=request.user.email).role

        return self.render_to_response(
            self.get_context_data(
                user_role=user_role,
                class_list=class_names,
                create_module_form=create_module_form,
            )
        )
