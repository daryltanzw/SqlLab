from django.db import connection
from django.views.generic import FormView

from SqlLabApp.forms.reviewtest import ReviewTestForm
from SqlLabApp.models import User, TestForClass


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

        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM ' + instructor_test_table)
                instructor_test_table = cursor.fetchall()
                cursor.execute('SELECT * FROM ' + student_test_table)
                student_test_table = cursor.fetchall()

        except ValueError as err:
            raise err

        finally:
            connection.close()

        questions = []
        answers = []
        marks = []
        correctness = []

        for i in range(0,len(instructor_test_table)):
            questions.append(str(i + 1) + ') ' + instructor_test_table[i][1])
            answers.append(student_test_table[i][2])
            marks.append(str(student_test_table[i][3]) + ' / ' + str(instructor_test_table[i][3]))

            if student_test_table[i][3] == instructor_test_table[i][3]:
                correctness.append(True)
            else:
                correctness.append(False)

        test_data = zip(questions, answers, marks, correctness)

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