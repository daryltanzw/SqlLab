from django.views.generic import FormView
from SqlLabApp.forms.testattempt import TestAttemptForm
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format, student_attempt_table_format
from django.db import connection

from SqlLabApp.models import User, UserRole, TestForClass, StudentAttemptsTest, QuestionAnswer
from SqlLabApp.utils.CryptoSign import encryptData
from SqlLabApp.utils.CryptoSign import decryptData

class TestAttemptFormView(FormView):
    form_class = TestAttemptForm
    template_name = 'SqlLabApp/testattempt.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        tid = self.kwargs['test_id']
        testid = int(decryptData(tid))

        test_attempt_list = list(reversed(StudentAttemptsTest.objects.filter(tid_id=testid,student_email_id=request.user.email)))
        test_name = TestForClass.objects.get(tid=testid).test_name
        user_role = UserRole.objects.get(email_id=request.user.email).role
        full_name = User.objects.get(email=request.user.email).full_name
        marks = []
        is_full_marks = []

        for tobj in test_attempt_list:
            with connection.cursor() as cursor:
                # Get table name
                student_test_name = student_attempt_table_format(testid, request.user.email, tobj.attempt_no)
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

            tobj.tid_id = encryptData(tobj.tid_id)

        test_attempt_list = zip(test_attempt_list, marks, is_full_marks)

        return self.render_to_response(
            self.get_context_data(
                full_name=full_name,
                user_role=user_role,
                testid=tid,
                test_name=test_name,
                test_attempt_list=test_attempt_list
            )
        )