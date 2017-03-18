from django.contrib.auth import login as django_login
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect

from SqlLabApp.forms.login import LoginForm
from SqlLabApp.forms.register import RegistrationForm
from SqlLabApp.backends import EmailAuthBackend


class MainView(TemplateView):
    template_name = 'SqlLabApp/loginregister.html'

    def get(self, request, *args, **kwargs):
        login_form = LoginForm(self.request.GET or None)
        register_form = RegistrationForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['register_form'] = register_form
        context['login_form'] = login_form
        return self.render_to_response(context)


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'SqlLabApp/loginregister.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(request.POST)
        register_form = RegistrationForm()
        if login_form.is_valid():
            auth = EmailAuthBackend()
            user = auth.authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect("../instructormodule")

        else:
            return self.render_to_response(
                self.get_context_data(
                    login_form=login_form,
                    register_form=register_form
                )
            )


class RegistrationFormView(FormView):
    form_class = RegistrationForm
    template_name = 'SqlLabApp/loginregister.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        register_form = self.form_class(request.POST)
        login_form = LoginForm()
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect("../instructormodule")

        else:
            return self.render_to_response(
                self.get_context_data(
                    register_form=register_form,
                    login_form=login_form
                )
            )
