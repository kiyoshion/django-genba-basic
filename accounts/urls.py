from django.urls import path

from django.views.generic import RedirectView, TemplateView
from . import views

app_name = 'accounts'
urlpatterns = [
  path('register/', RedirectView.as_view(url='/'), name='register'),
  path('login/', views.login, name='login'),
  path('logout/', RedirectView.as_view(url='/'), name='logout'),
  path('profile/', RedirectView.as_view(url='/'), name='profile'),
]
