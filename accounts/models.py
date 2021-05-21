from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in

class CustomUser(AbstractUser):
  class Meta(object):
    db_table = 'custom_user'

  login_count = models.IntegerField(verbose_name='ログイン回数', default=0)

  def post_login(self):
    self.login_count += 1
    self.save()
