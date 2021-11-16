"""MetroEvents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from administration.views import AdminView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('user.urls', namespace='user'), name='home'),
    path('home/', include('user.urls', namespace='user')),
    path('administration/', include('administration.urls', namespace='administration')),
    path('organizer/', include('organizer.urls', namespace='organizer')),
    path("admin/", AdminView.as_view(), name="admin_view"),
    path('api/', include('api.urls')),
]
