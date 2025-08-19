"""
User Profile Models for Django Authentication Service.

This module extends Django's built-in User model with custom profile fields
for production-ready user management with PostgreSQL 18 backend.
"""
# Signal to create/update profile when User is created/updated
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid
from django.utils import timezone


class HomePageInformation(models.Model):
    TAB_CHOICES = [
        ('instructions', 'Instructions'),
        ('offline', 'Offline'),
        ('downloads', 'Downloads'),
        ('publications', 'Publications'),
    ]

    tab_type = models.CharField(max_length=20, choices=TAB_CHOICES)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'information_home_page'

    def __str__(self):
        return f"{self.tab_type}: {self.title }"

class Feedback(models.Model):
    module = models.CharField(max_length=90)

    remarks = models.CharField(max_length=900, blank=True, null=True)
    insert_datetime = models.DateTimeField(default=timezone.now)
    modified_datetime = models.DateTimeField(blank=True)
    username = models.CharField(max_length=50)
    is_active = models.IntegerField(default=1)
    personal_no = models.CharField(max_length=50, blank=True, null=True)

    question1 = models.CharField(max_length=10, blank=True, null=True)
    question2 = models.CharField(max_length=10, blank=True, null=True)
    question3 = models.CharField(max_length=10, blank=True, null=True)
    question4 = models.CharField(max_length=10, blank=True, null=True)
    avg_feedback = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'tbl_usermgmt_feedback'

    def __str__(self):
        return f"{self.username} - Avg: {self.avg_feedback}"

class RoleMaster(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    status = models.IntegerField(default=1)  # Default to active (1)

    class Meta:
        db_table = 'tbl_role_master'

    def __str__(self):
        return f"{self.name} ({self.level})"

class UserDetails(models.Model):

    update_date = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    userlogin = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=510)
    confirm_password = models.CharField(max_length=510)
    personal_no = models.CharField(max_length=50)
    designation = models.CharField(max_length=100)
    designation_email = models.EmailField(max_length=150)
    ship_name = models.CharField(max_length=100)
    employee_type = models.CharField(max_length=50)
    establishment = models.CharField(max_length=100)
    nudemail = models.EmailField(max_length=150)
    phone_no = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=20)
    sso_user = models.CharField(max_length=1, default='0')
    H = models.CharField(max_length=1, default='0')
    L = models.CharField(max_length=1, default='0')
    E = models.CharField(max_length=1, default='0')
    X = models.CharField(max_length=1, default='0')
    status = models.CharField(max_length=1, default='1')
    
    
    class Meta:
        db_table = 'tbl_user_details'

    def __str__(self):
        return f"{self.user_login} ({self.name})"

    @property
    def is_authenticated(self):
        return True