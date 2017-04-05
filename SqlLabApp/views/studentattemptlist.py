from django.views.generic import FormView
from SqlLabApp.forms.testattempt import TestAttemptForm
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format, student_attempt_table_format
from django.db import connection

from SqlLabApp.models import User, UserRole, TestForClass, ClassTeacherTeaches, ClassStudentAttends, StudentAttemptsTest
from SqlLabApp.utils.CryptoSign import encryptData, decryptData


class StudentListFormView(FormView):
    form_class = TestAttemptForm
    template_name = 'SqlLabApp/studentattemptlist.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        tid = self.kwargs['test_id']
        testid = int(decryptData(tid))
        test_name = TestForClass.objects.get(tid=testid).test_name
        max_attempt = TestForClass.objects.get(tid=testid).max_attempt
        classid = TestForClass.objects.get(tid=testid).classid_id
        curr_full_name = User.objects.get(email=request.user.email).full_name
        teacher_list = ClassTeacherTeaches.objects.filter(classid_id=classid).values('teacher_email_id')
        student_list = ClassStudentAttends.objects.filter(classid_id=classid).values('student_email')
        user_name = []
        highest_marks = []
        is_highest_marks_full = []
        number_of_attempts = []
        attempt_list = []
        email_list = []

        for teacher in teacher_list:
            email_list.append(teacher['teacher_email_id'])

        for student in student_list:
            email_list.append(student['student_email'])

        user_id = list(range(0, len(email_list)))

        try:
            with connection.cursor() as cursor:
                instructor_test_name = test_name_table_format(testid, test_name)
                cursor.execute('SELECT SUM(marks) FROM ' + instructor_test_name)
                total_marks = cursor.fetchone()[0]

                for email in email_list:
                    user_exist = User.objects.filter(email=email).count() == 1

                    if user_exist:
                        user_name.append(User.objects.get(email=email).full_name.upper)
                        test_attempt_list = list(
                            reversed(StudentAttemptsTest.objects.filter(tid_id=testid, student_email_id=email)))
                        curr_number_of_attempts = len(test_attempt_list)
                        curr_highest_mark = 0

                        marks = []
                        is_full_marks = []
                        table_name = []

                        for tobj in test_attempt_list:
                            student_test_name = student_attempt_table_format(testid, email, tobj.attempt_no)
                            cursor.execute('SELECT SUM(marks) FROM ' + student_test_name)
                            student_marks = cursor.fetchone()[0]

                            marks.append(str(student_marks) + ' / ' + str(total_marks))

                            if student_marks == total_marks:
                                is_full_marks.append(True)
                            else:
                                is_full_marks.append(False)

                            # Check for highest mark for current student
                            if student_marks > curr_highest_mark:
                                curr_highest_mark = student_marks

                            # curr_name = encryptData(str(instructor_test_name + '-' + student_test_name))
                            curr_name = str(instructor_test_name + '-' + student_test_name)
                            table_name.append(curr_name)

                        if curr_highest_mark == total_marks:
                            is_highest_marks_full.append(True)
                        else:
                            is_highest_marks_full.append(False)

                        tobj.tid_id = encryptData(tobj.tid_id)
                        highest_marks.append(str(curr_highest_mark))
                        number_of_attempts.append(str(curr_number_of_attempts) + ' / ' + str(max_attempt))
                        test_attempt_list = zip(test_attempt_list, marks, table_name, is_full_marks)
                        attempt_list.append(test_attempt_list)

        except ValueError as err:
            raise err

        finally:
            connection.close()

        user_list = zip(user_id, user_name, attempt_list, highest_marks, is_highest_marks_full, number_of_attempts)

        return self.render_to_response(
            self.get_context_data(
                testid=tid,
                test_name=test_name,
                full_name=curr_full_name,
                user_list=user_list,
                total_marks=total_marks
            )
        )
