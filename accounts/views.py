from django.shortcuts import render, redirect
from django.views import View

class LoginView(View):
  def get(self, request, *args, **kwargs):
    context = {
      'msg': 'Hello'
    }
    return render(request, 'index.html', context)

login = LoginView.as_view()
