from __future__ import unicode_literals
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=3)

    USERNAME_FIELD = 'email'

    def set_role(self, role):
        self.role = role

    def get_role(self):
        return self.role

    def get_short_name(self):
        pass

    def get_full_name(self):
        pass

# class Test(models.Model):
#     ins_email_id =