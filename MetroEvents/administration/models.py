from django.db import models
from datetime import datetime
from django.utils import timezone
from user.models import User
from organizer.models import Organizer
# Create your models here.

class Administrator(User):
	admin_id = models.AutoField(primary_key=True)
	date_accepted = models.DateField(auto_now=True)
	class Meta:
		db_table="Administrator"

class Event(models.Model):
	event_id = models.AutoField(primary_key=True)
	organizer = models.ForeignKey(Organizer, null = False, blank = False, on_delete = models.CASCADE, related_name = "event_organizer")
	title = models.CharField(max_length=500, default="No Title")
	time = models.TimeField(auto_now=True)
	date = models.DateField(auto_now=True)
	location = models.CharField(max_length=500)
	description = models.CharField(max_length=1000, default="")
	status = models.BooleanField(default=True)
	event_type = models.CharField(max_length=100)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		db_table="Event"

class Participants(models.Model):
	participant_id = models.AutoField(primary_key=True)
	event_id = models.ForeignKey(Event, null = False, blank = False, on_delete = models.CASCADE, related_name = "event_joined")
	user_id = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE, related_name = "participant")
	date_joined = models.DateField(auto_now=True)
	# hasJoined = models.BooleanField(default=False)
	isAccepted = models.BooleanField(default=False)
	class Meta:
		db_table="Participants"

class Comment(Participants):
	comment_id = models.AutoField(primary_key=True)
	content = models.CharField(max_length=500)
	date_comment = models.DateField(auto_now=True)
	class Meta:
		db_table="Comment"