from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.

class XssView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'xss.html', {})