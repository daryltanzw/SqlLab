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


class Test(models.Model):
    ins_email = models.ForeignKey(User)
    tid = models.IntegerField(primary_key=True)
    test_table_name = models.CharField(max_length=100, null=False)  # reflects an actual table


# Created on the fly from test_table_name
# class Question(models.Model):
#     question_id = models.IntegerField(primary_key=True)
#     question_name = models.CharField(max_length=100, null=False)
#     teacher_ans_query = models.TextField(null=False)


class QuestionData(models.Model):
    class Meta:
        unique_together = (('tid', 'data_tbl_name'),)

    tid = models.ForeignKey(Test)
    data_tbl_name = models.CharField(max_length=100)
    student_visible = models.BooleanField(default=True)
