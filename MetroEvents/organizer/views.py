from django.shortcuts import render, redirect
from django.shortcuts import render
from django.core import serializers
from django.views.generic import View, TemplateView
from .models import *
from administration.models import Event, Participants
from user.models import Notification
from django.http import JsonResponse
from user.models import User
# Create your views here.
class OrganizerView(View):
	def get(self, request):
		user_id = request.session['user_id']
		#event_query = Event.objects.raw("select event_id from event inner join participants on participants.user_id_id = %s group by event.event_id;", [user_id])
		# for ee in event_query:
		# 	event_id = ee.event_id
		notjoins = Event.objects.raw("select * from event where event_id NOT IN (select event.event_id from event inner join participants on event.event_id = participants.event_id_id and participants.user_id_id = %s group by event.event_id);", [user_id])
		notifications = Notification.objects.raw("select * from notification where notification.isRead = 0 and notification.receiver= %s Limit 5;", [user_id])

		context =  {
		'user_id':user_id,
		'notjoins': notjoins,
		'notifications': notifications,
		}
		return render(request, 'organizer/Organizer.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'organizer/CreatedEvents.html', {'requestOrganizer': response_data})
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
			return redirect('user:organizer_view')

class AddEventView(View):
	def get(self, request):
		user_id = request.session['user_id']
		org_ids = Organizer.objects.raw("select * from organizer inner join user where organizer.user_ptr_id = %s;", [user_id])
		notifications = Notification.objects.raw("select * from notification where notification.isRead = 0 and notification.receiver= %s Limit 5;", [user_id])
		
		for org in org_ids:
			organizer_id = org.org_id
		context =  {
		'user_id':user_id,
		'organizer_id': organizer_id,
		'notifications': notifications,
		}
		return render(request, 'organizer/AddEvent.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'organizer/CreatedEvents.html', {'requestOrganizer': response_data})
		elif request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")
		org_id =  request.POST.get("org_id")
		title =  request.POST.get("event_title")
		date = request.POST.get("date")
		time = request.POST.get("time")
		location = request.POST.get("location")
		description = request.POST.get("description")
		event_type = request.POST.get("event_type")
		Event.objects.create(organizer_id = org_id, title=title, 
		 	date=date, time= time, location=location, description=description, event_type=event_type, status=True)
		print(event_type)
		return redirect('organizer:createdEvents_view')

class ManageParticipantsView(View):
	def get(self, request):
		user_sh = request.session['user_id']
		users = User.objects.raw("select * from user inner join request where user.user_id = request.sender_id and request.status='Pending';")
		# for user in users:
		# 	print(user.sender_id)
		context =  {
		'user_sh':user_sh,
		'users':users
		}
		return render(request, 'organizer/ManageParticipants.html', context)
	def post(self, request):
		user_id = request.POST.get("user_id")
		request_type = request.POST.get("request_type")
		print(request_type)
		users = User.objects.filter(user_id=user_id)

		for user in users:
			if request_type == '0':
				if Organizer.objects.filter(user_id=user_id).exists():
					print("already exist")
				else:
					print("request for Organizer")
					Organizer.objects.create(user_ptr_id=user_id, firstname = user.firstname,
					middlename=user.middlename, lastname=user.lastname,  username=user.username,
					password=user.password, age = user.age)
				Request.objects.filter(sender_id=user_id, request_type=request_type).update(status="Accepted")
			elif request_type == '1':
				if Administrator.objects.filter(user_id=user_id).exists():
					print("already exist")
				else:
					print("request for admin")
					Administrator.objects.create(user_ptr_id=user_id, firstname = user.firstname,
					middlename=user.middlename, lastname=user.lastname,  username=user.username,
					password=user.password, age = user.age)
				Request.objects.filter(sender_id=user_id, request_type=request_type).update(status="Accepted")
		if request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")		

		return redirect('organizer:manageParticipants_view')
      
class CreatedEventsView(View):
	def get(self, request):
		user_id = request.session['user_id']
		user_sh = request.session['user_id']
		events = Event.objects.all()
		org_ids = Organizer.objects.raw("select * from organizer inner join user where organizer.user_ptr_id = %s Limit 5;", [user_sh])
		notifications = Notification.objects.raw("select * from notification where notification.isRead = 0 and notification.receiver= %s Limit 5;", [user_id])
		participants = User.objects.raw("select * from user inner join participants where participants.user_id_id = user.user_id;")
		for org in org_ids:
			organizer_id = org.org_id
			
		context =  {
		'user_sh':user_sh,
		'user_id':user_id,
		'events':events,
		'org_id':organizer_id,
		'notifications': notifications,
		'participants' : participants,
		}
		return render(request, 'organizer/CreatedEvents.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'organizer/CreatedEvents.html', {'requestOrganizer': response_data})

		if request.method == 'POST':
			if 'deleteEvent' in request.POST:
				print('delete button clicked')
				eventID = request.POST.get("event-event_id")
				deleteEvent = Event.objects.filter(event_id=eventID).delete()
				print('recorded deleted') 
		if request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")
		return redirect('organizer:createdEvents_view')

class  MyEventsView(View):
	def get(self, request):
		user_id = request.session['user_id']
		events = Event.objects.raw("select * from event inner join participants on participants.event_id_id = event.event_id where participants.user_id_id = %s;", [user_id] )
		notifications = Notification.objects.raw("select * from notification where notification.isRead = 0 and notification.receiver= %s Limit 5;", [user_id])
		context =  {
		'events':events,
		'notifications':notifications,
		'user_id': user_id,
		}
		return render(request, 'organizer/organizerMyEvents.html', context)
	def post(self, request):
		response_data ={}
		if request.POST.get('action') == 'notifRead':
			notif_id = request.POST.get("notification_id")
			response_data["status"] = 1
			Notification.objects.filter(notification_id=notif_id).update(isRead=True)
			return JsonResponse(response_data)
			return render(request, 'organizer/CreatedEvents.html', {'requestOrganizer': response_data})
		elif request.POST.get('action') == 'logout':
			del request.session['user_id']
			return redirect("user:welcome_view")
		else:
			user_id =  request.POST.get("user_id")
			event_id = request.POST.get("event_id")
			#Participants.objects.raw("delete from participants where participants.user_id_id = %s and participants.event_id_id = %s;", [user_id], [event_id])
			delete_participant = Participants.objects.filter(user_id_id=user_id, event_id_id=event_id).delete()
			return redirect('organizer:myevents_view')