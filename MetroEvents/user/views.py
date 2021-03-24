from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from .models import *
from user.forms import UserForm
from django.http import JsonResponse
from django.http import HttpResponse
import json
import hashlib 
from administration.models import Administrator
from organizer.models import Organizer
from administration.models import Event
from django.core import serializers
from administration.models import Participants
# Create your views here.
class WelcomeView(View):
	def get(self, request):
		return render(request, 'user/LandingPage.html')
	def post(self, request):
		post = User.objects.all()
		data = {}
		user_id = -1
	#	form = UserForm(request.POST)
		response_data = {}
		if request.POST.get('action') == 'post':
			firstname = request.POST.get("firstname")
			middlename = request.POST.get("middlename")
			lastname = request.POST.get("lastname")
			username = request.POST.get("username")
			password = request.POST.get("password")
			md5pass = hashlib.md5(password.encode()) 
			password = md5pass.hexdigest()
			age = request.POST.get("age")
			response_data['result'] = 'Create post successful!'
			response_data['firstname'] = firstname
			response_data['middlename'] = middlename
			response_data['lastname'] = lastname
			response_data['username'] = username
			response_data['password'] = password
			response_data['age'] = age
			# form = User(firstname = firstname, middlename = middlename, lastname = lastname, username = username, password = password, age = age)
			# form.save()
			user = User.objects.create(firstname = firstname, middlename = middlename, lastname = lastname, username = username, password = password, age = age)
			user.save()
			return JsonResponse(response_data)
			return render(request, 'user/LandingPage.html', {'post':post})
		elif request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")
		elif request.POST.get('action') == 'postLogin':
			username = request.POST.get("username")
			password = request.POST.get("password")
			md5pass = hashlib.md5(password.encode()) 
			password = md5pass.hexdigest()
			user = User.objects.filter(username = username)
			response_data["status"] = 0
			for p in user:
				if p.password == password:
					response_data["status"] = 1
					user_id = p.user_id
			
			if Organizer.objects.filter(user_ptr_id=user_id).exists():
				response_data["status"] = 3
			elif Administrator.objects.filter(user_ptr_id=user_id).exists():
				response_data["status"] = 2			


			request.session['user_id'] = user_id
			# usernameLogin = User.objects.raw("select user_id from user where username = %s;", [username])
			

			
			# for p in usernameLogin:
			# 	print("user id: "+ str(p.user_id))
		
			# data = serializers.serialize('json', list(usernameLogin))
			# print(data)
			# return JsonResponse(data, safe=False)
			# return render(request, 'user/LandingPage.html', {'postLogin': "dddd"})
	
			return JsonResponse(response_data)
			return render(request, 'user/LandingPage.html', {'postLogin': response_data})


class UserView(View):
	def get(self, request):
		user_id = request.session['user_id']
		#event_query = Event.objects.raw("select event_id from event inner join participants on participants.user_id_id = %s group by event.event_id;", [user_id])
		# for ee in event_query:
		# 	event_id = ee.event_id
		notjoins = Event.objects.raw("select * from event where event_id NOT IN (select event.event_id from event inner join participants on event.event_id = participants.event_id_id and participants.user_id_id = %s group by event.event_id);", [user_id])
		notifications = Notification.objects.raw("select * from notification where (notification.subject = '0'  or notification.subject = '-1') and notification.isRead = 0 and notification.receiver= %s;", [user_id])

		context =  {
		'user_sh':user_id,
		'notjoins': notjoins,
		'notifications': notifications 
		}
		return render(request, 'user/User.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'user/UserRequest.html', {'requestOrganizer': response_data})
		elif request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")
		user_id = request.POST.get("user_id")
		event_id = request.POST.get("event_id")
		events = Event.objects.all()
		Participants.objects.create(user_id_id=user_id, event_id_id = event_id)
		queries = Event.objects.raw("select * from event inner join organizer on event.organizer_id = organizer.org_id and event.event_id = %s;", [event_id])
		user = User.objects.filter(user_id=user_id);
		for q in queries:
			receiver_id = q.user_ptr_id
		for u in user:
			notif_content = u.firstname+" joined your event"
		Notification.objects.create(sender_id = user_id, content = notif_content, receiver = receiver_id)
		context =  {
		'user_sh':user_id,
		'events': events
		}
		print(event_id) 
		return redirect('user:user_view')


class RequestView(View):

	def get(self, request):
		user_id = request.session['user_id']
		requests = Request.objects.raw("select * from request where sender_id = %s;", [user_id])
		notifications = Notification.objects.raw("select * from notification where (notification.subject = '0'  or notification.subject = '-1') and notification.isRead = 0 and notification.receiver= %s;", [user_id])
		context =  {
		'user_sh':user_id,
		'requests':requests,
		'notifications': notifications,
		}
		return render(request, 'user/UserRequest.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'user/UserRequest.html', {'requestOrganizer': response_data})
		elif request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")		
		elif request.POST.get('action') == 'requestOrganizer':
			user_id = request.POST.get("user_id")
			users = User.objects.filter(user_id = user_id)
			content = "Request for Organizer Account"
			for user in users:
				notif_content = user.firstname+" sent you a request for organizer account"
			Request.objects.create(sender_id = user_id, content = content)
			Notification.objects.create(sender_id = user_id, content = notif_content)
			response_data["status"] = 1
			return JsonResponse(response_data)
			return render(request, 'user/UserRequest.html', {'requestOrganizer': response_data})
		elif request.POST.get('action') == 'requestAdmin':
			user_id = request.POST.get("user_id")
			users = User.objects.filter(user_id = user_id)
			content = "Request for Administrator Account"
			for user in users:
				notif_content = user.firstname+" sent you a request for admin account"
			request_type = 1
			Request.objects.create(sender_id = user_id, content = content, request_type= request_type)
			Notification.objects.create(sender_id = user_id, content = notif_content)
			response_data["status"] = 1
			return JsonResponse(response_data)
			return render(request, 'user/UserRequest.html', {'requestOrganizer': response_data})

class MyEventsView(View):
	def get(self, request):
		user_id = request.session['user_id']
		events = Event.objects.raw("select * from event inner join participants on participants.event_id_id = event.event_id where participants.user_id_id = %s;", [user_id] )
		notifications = Notification.objects.raw("select * from notification where (notification.subject = '0'  or notification.subject = '-1') and notification.isRead = 0 and notification.receiver= %s;", [user_id])
		context =  {
		'events':events,
		'notifications':notifications,
		'user_id': user_id,
		}
		return render(request, 'user/userMyEvents.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'user/UserRequest.html', {'requestOrganizer': response_data})
		elif request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")
		else:
			user_id =  request.POST.get("user_id")
			event_id = request.POST.get("event_id")
			#Participants.objects.raw("delete from participants where participants.user_id_id = %s and participants.event_id_id = %s;", [user_id], [event_id])
			delete_participant = Participants.objects.filter(user_id_id=user_id, event_id_id=event_id).delete()
			return redirect('user:myevents_view')



