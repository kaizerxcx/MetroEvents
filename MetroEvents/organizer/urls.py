from django.contrib import admin
from django.urls import include,path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'organizer'
urlpatterns = [
	path("addEvent", views.AddEventView.as_view(), name="addEvent_view"),
    path("manageParticipants", views.ManageParticipantsView.as_view(), name="manageParticipants_view"),
    path("createdEvents", views.CreatedEventsView.as_view(), name="createdEvents_view"),
     path("myEvents", views.MyEventsView.as_view(), name="myevents_view"),
]
