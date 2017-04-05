import operator

from SqlLabApp.forms.module import InstructorModuleForm
from django.views.generic import FormView
from SqlLabApp.models import User, UserRole, Class, ClassTeacherTeaches, ClassStudentAttends
from SqlLabApp.utils.CryptoSign import encryptData


class InstructorModuleFormView(FormView):
    form_class = InstructorModuleForm
    template_name = 'SqlLabApp/module.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        create_module_form = InstructorModuleForm
        user_role = UserRole.objects.get(email_id=request.user.email).role
        full_name = User.objects.get(email=request.user.email).full_name
        if user_role == 'INS':
            class_list = ClassTeacherTeaches.objects.filter(teacher_email_id=request.user.email)
        else:  # STU
            class_list = ClassStudentAttends.objects.filter(student_email=request.user.email)

        class_names = []
        number_of_students = []

        for module in class_list:
            class_names.append(Class.objects.get(classid=module.classid_id))

        for cobj in class_names:
            student_list = ClassStudentAttends.objects.filter(classid_id=cobj.classid)
            number_of_students.append(len(student_list))
            cobj.classid = encryptData(cobj.classid)

        class_names.sort(key=operator.attrgetter('class_name'))
        class_list = zip(class_names, number_of_students)

        return self.render_to_response(
            self.get_context_data(
                full_name=full_name,
                user_role=user_role,
                class_list=class_list,
                create_module_form=create_module_form,
            )
        )
