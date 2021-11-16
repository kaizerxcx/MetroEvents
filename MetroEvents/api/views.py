from django.shortcuts import render
from django.core.serializers import serialize
from django.shortcuts import render
from user.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer

# Create your views here.

@api_view(['GET'])
def getAllUser(request):
	user = User.objects.all()
	serializer = UserSerializer(user, many=True)
	return Response(serializer.data)

@api_view(['POST'])
def getUser(request, pk):
	user = User.objects.filter(user_id=pk)
	serializer = UserSerializer(user, many=True)
	return Response(serializer.data)