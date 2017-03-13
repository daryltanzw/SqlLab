from django.views.generic import FormView

from SqlLabApp.forms.createtest import CreateTestForm

class CreateTestFormView(FormView):
    form_class = CreateTestForm
    template_name = 'SqlLabApp/createtest.html'
    success_url = '/'