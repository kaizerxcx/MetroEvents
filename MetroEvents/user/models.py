from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=100)
	middlename = models.CharField(max_length=100, default="NA")
	lastname = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	age = models.IntegerField(default=3)
	date_registered = models.DateField(auto_now=True)
	class Meta:
		db_table="User"


class Notification(models.Model):
	notification_id = models.AutoField(primary_key=True)
	sender = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE, related_name = "notification_sender")
	receiver = models.CharField(max_length=500)
	content = models.CharField(max_length=500)
	subject = models.CharField(max_length=100)
	time = models.TimeField(auto_now=True)
	date = models.DateField(auto_now=True)
	isRead = models.BooleanField(default=False)
	class Meta:
		db_table="Notification"

class Request(models.Model):
	request_id = models.AutoField(primary_key=True)
	sender = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE, related_name = "request_sender")
	receiver =  models.CharField(max_length=500)
	content = models.CharField(max_length=500)
	status = models.CharField(max_length=100, default="Pending")
	time = models.TimeField(auto_now=True)
	date = models.DateField(auto_now=True)
	isRead = models.BooleanField(default=False)
	request_type = models.IntegerField(default=0)
	class Meta:
		db_table="Request"

