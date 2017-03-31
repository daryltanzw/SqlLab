from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from SqlLabApp.forms.teacher_manage_module import TeacherManageModule
from SqlLabApp.models import User, ClassStudentAttends
from SqlLabApp.utils.CryptoSign import decryptData, encryptData


class TeacherManageModuleFormView(FormView):
    form_class = TeacherManageModule
    template_name = 'SqlLabApp/teacher_manage_module.html'

    def get(self, request, *args, **kwargs):
        full_name = User.objects.get(email=request.user.email).full_name
        cid = self.kwargs['class_id']
        classid = int(decryptData(cid))
        student_list = ClassStudentAttends.objects.filter(classid_id=classid).values('student_email')
        processed_student_list = []

        for studentobj in student_list:
            stu = str(studentobj['student_email'])
            stu_exist = User.objects.filter(email=stu).count() == 1
            if stu_exist:
                s = str(stu + "\t" + User.objects.get(email=stu).full_name)
                processed_student_list.append(s)
            else:
                processed_student_list.append(stu)

        return self.render_to_response(
            self.get_context_data(
                full_name=full_name,
                processed_student_list=processed_student_list
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


