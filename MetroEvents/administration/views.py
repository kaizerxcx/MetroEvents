from django.shortcuts import render, redirect
from django.core import serializers
from django.views.generic import View, TemplateView
from .models import *
from user.models import Request, Notification
from organizer.models import Organizer
from django.http import JsonResponse

# Create your views here.
class AdminView(View):
	def get(self, request):
		user_id = request.session['user_id']
		notifications = Notification.objects.raw("select * from notification where isRead = 0 and notification.receiver < 1 limit 5;")
		notjoins = Event.objects.raw("select * from event where event_id NOT IN (select event.event_id from event inner join participants on event.event_id = participants.event_id_id and participants.user_id_id = %s group by event.event_id);", [user_id])
		context =  {
		'user_id':user_id,
		'notifications':notifications,
		'notjoins':notjoins,
		}
		return render(request, 'admin/AdminHome.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'admin/AdminRequest.html', {'requestOrganizer': response_data})
		elif request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")
		else:
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
			return redirect('user:admin_view')



# Create your views here.
class ManageRequestView(View):
	def get(self, request):
		user_sh = request.session['user_id']
		users = User.objects.raw("select * from user inner join request where user.user_id = request.sender_id and request.status='Pending';")
		notifications = Notification.objects.raw("select * from notification where isRead = 0 and notification.receiver < 1 limit 5;")
		# for user in users:
		# 	print(user.sender_id)
		context =  {
		'user_sh':user_sh,
		'users':users,
		'notifications':notifications,
		}
		return render(request, 'admin/AdminRequest.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'admin/AdminRequest.html', {'requestOrganizer': response_data})
		elif request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")		

		user_id = request.POST.get("user_id")
		request_type = request.POST.get("request_type")
		print(request_type)
		users = User.objects.filter(user_id=user_id)
		sender_id = request.session['user_id']	
		for user in users:
			if request_type == '0':
				if Organizer.objects.filter(user_id=user_id).exists():
					print("already exist")
				else:
					print("request for Organizer")
					Organizer.objects.create(user_ptr_id=user_id, firstname = user.firstname,
					middlename=user.middlename, lastname=user.lastname,  username=user.username,
					password=user.password, age = user.age)
					content = "Organizer account accepted"
					subject = "0"
					Notification.objects.create(receiver=user_id, content=content, subject=subject, sender_id=sender_id)
				Request.objects.filter(sender_id=user_id, request_type=request_type).update(status="Accepted")
			elif request_type == '1':
				if Administrator.objects.filter(user_id=user_id).exists():
					print("already exist")
				else:
					print("request for admin")
					Administrator.objects.create(user_ptr_id=user_id, firstname = user.firstname,
					middlename=user.middlename, lastname=user.lastname,  username=user.username,
					password=user.password, age = user.age)
					content = "Administrator account accepted"
					subject = "-1"
					Notification.objects.create(receiver=user_id, content=content, subject=subject, sender_id=sender_id)
				Request.objects.filter(sender_id=user_id, request_type=request_type).update(status="Accepted")


		return redirect('administration:manageRequest_view')

class  MyEventsView(View):
	def get(self, request):
		user_id = request.session['user_id']
		events = Event.objects.raw("select * from event inner join participants on participants.event_id_id = event.event_id where participants.user_id_id = %s;", [user_id] )
		notifications = Notification.objects.raw("select * from notification where isRead = 0 and notification.receiver < 1 limit 5;")
		context =  {
		'events':events,
		'notifications':notifications,
		'user_id': user_id,
		}
		return render(request, 'admin/adminMyEvents.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'admin/AdminRequest.html', {'requestOrganizer': response_data})
		elif request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")	
		else:
			user_id =  request.POST.get("user_id")
			event_id = request.POST.get("event_id")
			#Participants.objects.raw("delete from participants where participants.user_id_id = %s and participants.event_id_id = %s;", [user_id], [event_id])
			delete_participant = Participants.objects.filter(user_id_id=user_id, event_id_id=event_id).delete()
			return redirect('administration:myEvents_view')



