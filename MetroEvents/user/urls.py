from django.contrib import admin
from django.urls import include,path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from administration.views import AdminView
from organizer.views import OrganizerView

app_name = 'user'
urlpatterns = [
  path('', views.WelcomeView.as_view(), name="welcome_view"),
  path("admin", AdminView.as_view(), name="admin_view"),
  path("organizer", OrganizerView.as_view(), name="organizer_view"),
  path("user", views.UserView.as_view(), name="user_view"),
  path("request", views.RequestView.as_view(), name="request_view"),
  path("myEvents", views.MyEventsView.as_view(), name="myevents_view"),
 ]
