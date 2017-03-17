from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100, null=False)
    full_name = models.CharField(max_length=100, default="", null=False)
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.full_name

    def set_full_name(self, fname):
        self.full_name = fname

    def get_short_name(self):
        pass

    def get_full_name(self):
        pass


class UserRole(models.Model):
    class Meta:
        unique_together = (('email', 'role'),)
    email = models.ForeignKey(User)
    role = models.CharField(max_length=3)


class Class(models.Model):
    classid = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100, null=False)


class ClassTeacherTeaches(models.Model):
    class Meta:
        unique_together = (('classid', 'teacher_email'),)
    classid = models.ForeignKey(Class)
    teacher_email = models.ForeignKey(User)


class ClassStudentAttends(models.Model):
    class Meta:
        unique_together = (('classid', 'student_email'),)
    classid = models.ForeignKey(Class)
    student_email = models.ForeignKey(User)


class TestForClass(models.Model):
    tid = models.AutoField(primary_key=True)
    classid = models.ForeignKey(Class)
    start_time = models.DateTimeField(default=datetime.now, blank=True)
    end_time = models.DateTimeField(default=datetime.now, blank=True)
    test_name = models.CharField(max_length=100, null=False)
    max_attempt = models.IntegerField(null=True, default=None) #if null, assume unlimited
    # dyanmic Sql Table is created "tid1.test_name" to store all Questions


class StudentAttemptsTest(models.Model):
    class Meta:
        unique_together = (('tid', 'student_email', 'attempt_no'),)

    tid = models.ForeignKey(TestForClass)
    student_email = models.ForeignKey(User)
    attempt_no = models.IntegerField()
    total_marks = models.IntegerField()
    student_attempt_tbl_name = models.CharField(max_length=100, null=False)
    # dynamic Sql Table is created "student_email.tid1" to store students answers


class QuestionDataUsedByTest(models.Model):
    class Meta:
        unique_together = (('tid', 'data_tbl_name'),)

    tid = models.ForeignKey(TestForClass)
    data_tbl_name = models.CharField(max_length=100, null=False)
    student_visibility = models.BooleanField(default=True)
    # dyanamic Sql Table is created "tid1.Employee1" to store Data tables which will be queried against.

