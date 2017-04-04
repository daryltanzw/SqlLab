import itertools as it

from django.db import connection
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from SqlLabApp.forms.reviewtest import ReviewTestForm
from SqlLabApp.models import User, QuestionAnswer, TestForClass, StudentAttemptsTest, QuestionDataUsedByTest
from SqlLabApp.utils.CreateStudentAttemptTable import create_student_attempt_table
from SqlLabApp.utils.CryptoSign import decryptData
from SqlLabApp.utils.CryptoSign import encryptData
from SqlLabApp.utils.DBUtils import get_db_connection
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format, student_attempt_table_format


class ReviewTestFormView(FormView):
    form_class = ReviewTestForm
    template_name = 'SqlLabApp/reviewtest.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        tables = self.kwargs['tables']
        # tables = str(decryptData(tables))
        tables = tables.split('-')
        full_name = User.objects.get(email=request.user.email).full_name

        # Get q/a tables
        instructor_test_table = tables[0]
        student_test_table = tables[1]

        # Get tid
        tidname = instructor_test_table.split('_')[0]        #i.e tid100
        tid = int(tidname.split('tid', 1)[1])                #i.e 100

        take_test_form = ReviewTestForm
        test_name = TestForClass.objects.get(tid=tid).test_name

        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM ' + instructor_test_table)
            instructor_test_table = cursor.fetchall()
            cursor.execute('SELECT * FROM ' + student_test_table)
            student_test_table = cursor.fetchall()

        questions = []
        answers = []
        marks = []
        qn_id = 0

        for instructor, student in instructor_test_table, student_test_table:
            qn_id += 1
            questions.append(str(qn_id) + ". " + str(instructor[1]))
            print "=========="
            print instructor[1]
            answers.append(student[0])
            print student[0]
            marks.append(str(student[3]) + ' / ' + str(instructor[3]))
            print str(student[3]) + ' / ' + str(instructor[3])

        test_data = zip(questions, answers, marks)

        return self.render_to_response(
            self.get_context_data(
                full_name=full_name,
                instructor_test_table=instructor_test_table,
                student_test_table=student_test_table,
                take_test_form=take_test_form,
                test_name=test_name,
                test_data=test_data
            )
        )