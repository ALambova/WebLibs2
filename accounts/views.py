from django.shortcuts import render, HttpResponse, redirect
from . import forms
from users.models import Library, LibUser
from registration.views import RegistrationView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class LibraryRegistrationView(RegistrationView):
    form_class = forms.LibraryRegistrationForm
    template_name = 'template.html'

    def register(self, form):
        user = Library.objects.create_user(
                username=self.request.POST['username'],
                email=self.request.POST['email'],
                password=self.request.POST['password1'],
                address=self.request.POST['address'],
                phoneNum=self.request.POST['phoneNum'],
                director=self.request.POST['director'],
                is_library=True)
        return user

    def get_success_url(self, user):
        return 'http://127.0.0.1:8000/accounts/login/'


class LibUserRegistrationView(RegistrationView):
    form_class = forms.LibUserRegistrationForm
    template_name = 'template.html'

    def register(self, form):
        user = LibUser.objects.create_user(
                username=self.request.POST['username'],
                email=self.request.POST['email'],
                password=self.request.POST['password1'],
                address=self.request.POST['address'],
                phoneNum=self.request.POST['phoneNum'])
        return user

    def get_success_url(self, user):
        return 'http://127.0.0.1:8000/accounts/login/'


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = 'http://127.0.0.1:8000/accounts/home/'
    template_name = 'template.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(LoginRequiredMixin, RedirectView):
    url = 'http://127.0.0.1:8000/accounts/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)


@login_required(login_url='/login')
def home(request, *args, **kwargs):
    user = request.user
    return HttpResponse("Hello, " + user.username)
