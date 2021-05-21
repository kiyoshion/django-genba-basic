from django.urls import path

from django.views.generic import RedirectView
# from . import views

app_name = 'shop'
urlpatterns = [
  path('', RedirectView.as_view(url='/'), name='index'),
  path('<int:book_id>/', RedirectView.as_view(url='/'), name='detail'),
  path('checkout/', RedirectView.as_view(url='/'), name='checkout'),
]
