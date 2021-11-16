from rest_framework import serializers
from user.models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields ='__all__'
		
class NotificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notification
		fields ='__all__'