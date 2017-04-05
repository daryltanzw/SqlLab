from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from SqlLabApp.forms.uploadstudentlist import TeacherManageModule
from SqlLabApp.models import User, Class, ClassStudentAttends
from SqlLabApp.utils.CryptoSign import decryptData, encryptData


class TeacherManageModuleFormView(FormView):
    form_class = TeacherManageModule
    template_name = 'SqlLabApp/uploadstudentlist.html'

    def get(self, request, *args, **kwargs):
        full_name = User.objects.get(email=request.user.email).full_name
        cid = self.kwargs['class_id']
        classid = int(decryptData(cid))
        module_name = Class.objects.get(classid=classid).class_name

        student_list = ClassStudentAttends.objects.filter(classid_id=classid).values('student_email')
        student_email_signedup = []
        student_email_notsignedup = []
        student_name_signedup = []
        student_name_notsignedup = []

        for studentobj in student_list:
            email = str(studentobj['student_email'])
            stu_exist = User.objects.filter(email=email).count() == 1

            if stu_exist:
                student_email_signedup.append(email)
                student_name_signedup.append(User.objects.get(email=email).full_name.upper)

            else:
                student_email_notsignedup.append(email)
                student_name_notsignedup.append('')

        student_signedup = zip(student_email_signedup, student_name_signedup)
        student_notsignedup = zip(student_email_notsignedup, student_name_notsignedup)

        return self.render_to_response(
            self.get_context_data(
                full_name=full_name,
                module_name=module_name,
                student_signedup=student_signedup,
                student_notsignedup=student_notsignedup
            )
        )

    def post(self, request, *args, **kwargs):
        teacher_manage_module_form = self.form_class(request.POST, request.FILES)
        cid = self.kwargs['class_id']
        classid = int(decryptData(cid))
        
        if teacher_manage_module_form.is_valid():
            student_list_file = request.FILES["student_list_file_upload"]

            if student_list_file is None:
                raise ValueError("No Upload for Student List File")

            student_list_file_lines = student_list_file.read().splitlines()

            try:
                with transaction.atomic():
                    ClassStudentAttends.objects.filter(classid_id=classid).delete()
                    for student in student_list_file_lines:
                        row = ClassStudentAttends(classid_id=classid, student_email=student)
                        row.save()

            except ValueError as err:
                raise err

            return HttpResponseRedirect("../teachermanagemodule/")

        else:
            raise ValueError(teacher_manage_module_form.errors)


