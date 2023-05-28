from argparse import ArgumentDefaultsHelpFormatter
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .models import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer    

class MyUserView(APIView):
    #POST user information and add him to database
    def post(self,request,*args,**kwargs):
        data = request.data
        try:
            if not data.contains("first_name"):
                return Response("First Name",status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                username = data['username'], 
                email = data['email'],
                password = make_password(data['password'])
            )
#            myuser = MyUser.objects.create(
#                user = user
#            )
            serializer = User_Serializer(user)
            
            return Response(serializer.data)
        except Exception as e: 
            print(e)
            message = {'detail' : 'There is already an account using this email or username.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    #GET user info by requested user
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"details":"Authentication credentials were not provided."},status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        

        serializer = User_Serializer(user)
        return Response(serializer.data)


class LocationsView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        #Get search parameters and return locations matching search
        pass
    @permission_classes([IsAuthenticated,IsAdminUser])
    def post(self, request, *args, **kwargs):
        #Check for admin user, and if so then add file data to database
        pass

class SingleLocationView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        #Get search parameters and return locations matching search
        pass


class SearchView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        #Get all searchs that the user is subscribed to
        pass
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        #Post new search
        pass
    @permission_classes([IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        #Remove search the search from saved searches
        pass

