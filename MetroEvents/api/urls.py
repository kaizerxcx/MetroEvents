from django.urls import path
from . import views

urlpatterns = [
	path('getAllUser/', views.getAllUser, name="users-list"),
	path('getUser/<str:pk>/', views.getUser, name="user-info"),
	path('getNotification/', views.getNotification, name="user-getNotification")

]