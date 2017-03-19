from django.views.generic import DetailView

from SqlLabApp.models import Class


class CreateTestFormView(DetailView):
    model = Class
    template_name = 'SqlLabApp/instructortest.html'
