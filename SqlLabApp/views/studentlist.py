from django.views.generic import FormView
from SqlLabApp.forms.testattempt import TestAttemptForm
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format, student_attempt_table_format
from django.db import connection

from SqlLabApp.models import User, UserRole, TestForClass, ClassStudentAttends, StudentAttemptsTest
from SqlLabApp.utils.CryptoSign import encryptData, decryptData

class StudentListFormView(FormView):
    form_class = TestAttemptForm
    template_name = 'SqlLabApp/studentlist.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        tid = self.kwargs['test_id']
        testid = int(decryptData(tid))
        test_name = TestForClass.objects.get(tid=testid).test_name
        classid = TestForClass.objects.get(tid=testid).classid_id
        curr_full_name = User.objects.get(email=request.user.email).full_name
        student_list = ClassStudentAttends.objects.filter(classid_id=classid)
        student_name = []
        student_attempt_list = []

        for student in student_list:
            stu_exist = User.objects.filter(email=student.student_email).count() == 1

            if stu_exist:
                student_name.append(User.objects.get(email=student.student_email).full_name.upper)

                test_attempt_list = list(reversed(StudentAttemptsTest.objects.filter(tid_id=testid, student_email_id=student.student_email)))
                test_name = TestForClass.objects.get(tid=testid).test_name
                full_name = User.objects.get(email=student.student_email).full_name
                marks = []
                is_full_marks = []
                table_name = []

                for tobj in test_attempt_list:
                    with connection.cursor() as cursor:
                        # Get table name
                        student_test_name = student_attempt_table_format(testid, student.student_email, tobj.attempt_no)
                        instructor_test_name = test_name_table_format(testid, test_name)

                        # Get total marks from instructor table
                        cursor.execute('SELECT SUM(marks) FROM ' + instructor_test_name)
                        total_marks = cursor.fetchone()[0]

                        # Get total marks from student table
                        cursor.execute('SELECT SUM(marks) FROM ' + student_test_name)
                        student_marks = cursor.fetchone()[0]

                        marks.append(str(student_marks) + ' / ' + str(total_marks))

                        if student_marks == total_marks:
                            is_full_marks.append(True)
                        else:
                            is_full_marks.append(False)

                        # curr_name = encryptData(str(instructor_test_name + '-' + student_test_name))
                        curr_name = str(instructor_test_name + '-' + student_test_name)
                        table_name.append(curr_name)

                test_attempt_list = zip(test_attempt_list, marks, table_name, is_full_marks)
                student_attempt_list.append(test_attempt_list)

            tobj.tid_id = encryptData(tobj.tid_id)

        student_list = zip(student_list, student_name, student_attempt_list)

        return self.render_to_response(
            self.get_context_data(
                testid=tid,
                test_name=test_name,
                full_name=curr_full_name,
                student_list=student_list
            )
        )