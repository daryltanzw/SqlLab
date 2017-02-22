from django.contrib.auth import login as django_login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from SqlLabApp.forms import AuthenticationForm
from SqlLabApp.forms.register import RegistrationForm
from SqlLabApp.backends import EmailAuthBackend


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth = EmailAuthBackend()
            user = auth.authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                django_login(request, user)
                return HttpResponse("Success Login")
    else:
        form = AuthenticationForm()

    return render(request, 'SqlLabApp/login.html', {'form': form, })


def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'SqlLabApp/register.html', {'form': form, })


