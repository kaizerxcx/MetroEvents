from django.db import models
from datetime import datetime
from django.utils import timezone
from user.models import User
# Create your models here.

class Organizer(User):
	org_id = models.AutoField(primary_key=True)
	date_accepted = models.DateField(auto_now=True)
	class Meta:
		db_table="Organizer"