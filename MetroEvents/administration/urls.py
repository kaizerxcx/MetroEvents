from django.contrib import admin
from django.urls import include,path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'administration'
urlpatterns = [
	path("manageRequest", views.ManageRequestView.as_view(), name="manageRequest_view"),
	path("myEvents", views.MyEventsView.as_view(), name="myEvents_view"),
]
