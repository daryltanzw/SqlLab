from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.db import models

from SqlLabApp.forms.taketest import TakeTestForm
from SqlLabApp.models import QuestionAnswer, TestForClass
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format

class TakeTestFormView(FormView):
    form_class = TakeTestForm
    template_name = 'SqlLabApp/taketest.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        take_test_form = TakeTestForm
        test_name = TestForClass.objects.get(tid=self.kwargs['test_id']).test_name
        test_name_table = test_name_table_format(self.kwargs['test_id'], test_name)
        qst_data = QuestionAnswer.objects.raw('SELECT * FROM ' + test_name_table)

        return self.render_to_response(
            self.get_context_data(
                take_test_form=take_test_form,
                test_name=test_name,
                qst_data=qst_data,
            )
        )
    '''    

    def post(self, request, *args, **kwargs):
        take_test_form = self.form_class(request.POST)
        if take_test_form.is_valid():
            take_test_form.save(request.user)
            return HttpResponseRedirect("../instructormodule")

        else:
            return self.render_to_response(
                self.get_context_data(
                    take_test_form=take_test_form,
                )
            )
    '''