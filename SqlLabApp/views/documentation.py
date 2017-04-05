from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

class DocumentationView(TemplateView):
    template_name = 'SqlLabApp/documentation.html'



