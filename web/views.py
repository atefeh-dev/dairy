from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes ,action
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
from rest_framework import status
import json


# Create your views here.
class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        print("yes")
        return Response(serializer.data)

    def create(self, request):
        if request.method == 'POST':
            print(request.data)
            serializer = UserSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                print("im here")
                serializer.save()
            return Response(serializer.data)

    def update(self, request, pk):
        print("im here in update ")
        if request.method == 'POST':
            user = User.objects.all().filter(id=pk)
            serializer = UserSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
