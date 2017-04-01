import os

from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from SqlLabApp.forms.createmodule import CreateModuleForm
from SqlLabApp.models import User, Class, ClassTeacherTeaches
from SqlLabApp.utils.DBUtils import get_db_connection


class CreateModuleFormView(FormView):
    form_class = CreateModuleForm
    template_name = 'SqlLabApp/createmodule.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        full_name = User.objects.get(email=request.user.email).full_name

        return self.render_to_response(
            self.get_context_data(
                full_name=full_name
            )
        )

    def post(self, request, *args, **kwargs):
        create_module_form = self.form_class(request.POST, request.FILES)

        if create_module_form.is_valid():
            class_name = request.POST['class_name']
            semester = request.POST['semester']
            facilitators = request.POST['facilitators']
            # student_list_file = request.POST['student_list_file']
            #
            # if student_list_file is None:
            #     raise ValueError("No Upload for student file")
            #
            # student_list_file_lines = student_list_file.read().splitlines()

            try:
                with transaction.atomic():
                    class_ = Class(class_name=class_name, semester=semester, facilitators=facilitators)
                    class_.save()

                    class_teacher_teaches = ClassTeacherTeaches(teacher_email_id=request.user.email, classid=class_)
                    class_teacher_teaches.save()

            except ValueError as err:
                raise err

            return HttpResponseRedirect("../module")

        else:
            raise ValueError(create_module_form.errors)


def validate_student_list_file(filename, q_a_file_lines):
    file_ext = os.path.splitext(filename)[1]
    valid_extensions = ['.tsv', '.txt']

    if file_ext.lower() not in valid_extensions:
        raise ValueError("Only tsv or txt files are allowed")

    for row in q_a_file_lines:
        splitted = row.split("\t")
        if len(splitted) != 2:
            raise ValueError("Expected Student Email <tab> Student Name".format(row))
