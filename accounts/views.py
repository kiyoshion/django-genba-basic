from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

class RegisterView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect(reverse('shop:index'))

    context = {
      'form': ResiterForm(),
    }
    return render(request, 'accounts/register.html', context)

  def post(self, request, *args, **kwargs):
    form = ResiterForm(reqeust.POST)

    if not form.is_valid():
      return render(reqeust, 'accounts/register.html', { 'form': form })

    user = form.save(commit=False)
    user.set_password(form.cleaned_data['password'])
    user.save()

    auth_login(request, user)

    return redirect(settings.LOGIN_REDIRECT_URL)

register = RegisterView.as_view()
class LoginView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect(reverse('shop:index'))

    context = {
      'form': LoginForm(),
    }
    return render(request, 'accounts/login.html', context)

  def post(self, request, *args, **kwargs):
    form = LoginForm(request.POST)

    if not form.is_valid():
      return render(request, 'accoutns.login.html', { 'form': form })

    user = form.get_user()

    auth_login(request, user)

    user.post_login()

    messages.info(request, "ログインしました。")

    return redirect(reverse('shop:index'))

login = LoginView.as_view()

class LogoutView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      auth_logout(request)

    messages.info(request, "ログアウトしました。")

    return redirect(reverse('accounts:login'))

logout = LogoutView.as_view()

class ProfileView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    form = ProfileForm(None, instance=request.user)
    context = {
      'form': form,
    }
    return render(request, 'accounts/profile.html', context)

  def post(self, request, *args, **kwargs):
    form = ProfileForm(request.POST, instance=request.user)
    if not form.is_valid():
      return render(request, 'accounts.profile.html', { 'form': form })

    form.save()

    messages.info(request, "プロフィールを更新しました。")
    return redirect('/accounts/profile/')

profile = ProfileView.as_view()
