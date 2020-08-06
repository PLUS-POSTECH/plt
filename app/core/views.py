from django.shortcuts import render, redirect
from django.contrib.auth import login
from django import forms
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .apps import init_sqli_db
from django.contrib.auth import get_user_model
from .models import SqliFilter
Team = get_user_model()

from utils.validator import unique_team_id

# use for check login...
# if needed something else, wonderful(ex. check login and also email?),,, use latter.
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.validator import LoginCheckMixin


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'core/index.html', {})


class RegisterForm(forms.Form):
    name = forms.CharField(validators=[unique_team_id])
    password = forms.CharField(min_length=8)
    email = forms.EmailField()


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {
            'form': form
        })

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'registration/register.html', {
                'form': form
            })

        team = Team.objects.create_user(
            name=form.cleaned_data['name'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email'],
        )

        init_sqli_db(team)
        login(request, team)
        return redirect('/')
