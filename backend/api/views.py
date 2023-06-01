from argparse import ArgumentDefaultsHelpFormatter
import csv
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from .serializers import *
from .models import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer    

# The class MyUserView is an API view that allows for creating and retrieving user information.
class MyUserView(APIView):
    #POST user information and add him to database
    def post(self,request,*args,**kwargs):
        data = request.data
        try:
            #if data.contains("first_name"):
            #   return Response("First Name",status=status.HTTP_400_BAD_REQUEST)
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
            serializer = UserSerializerWithToken(user, many = False)
            
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


# defines a view for creating and retrieving PointOfInterest objects with
# associated Category and Keyword objects.
class PointOfInterestView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        #Get search parameters and return locations matching search
        pointOfInterest = PointOfInterest.objects.all().order_by('-_id')
        
        serializer = PointOfInterestSerializer(pointOfInterest,many=True)
        
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        """
        This is a view function that creates a new PointOfInterest object with associated Category and
        Keyword objects, and returns a serialized representation of the created object.
        
        """
        # Check for admin user, and if not authenticated, return unauthorized response
        if not request.user.is_authenticated:
            return Response(
                {
                    "details":"User not authorized"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        if False and not request.user.is_staff:
            return Response(
                {
                    "details":"User has not staff privileges"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:    
            with transaction.atomic():
                user = request.user
                #this will change because the request.data will have the file containing this data
                upload_file = request.FILES.get('file')
                if upload_file is None:
                    return Response('No file was uploaded.',status=status.HTTP_400_BAD_REQUEST)
                
                upload_file=upload_file.read().decode('utf-8').replace('\r','')
                #print(upload_file)
                rows=upload_file.split('\n')
                for row in rows:
                    csv_entries=row.split(',')
                # **** here a function call will take place to return the fields from execl file ****
                    #print(csv_entries)
                # Create a new PointOfInterest object with the provided data
                    pois = PointOfInterest.objects.create (
                        user = user,
                        title =  csv_entries[0],
                        description = csv_entries[1],
                        latitude = float(csv_entries[2]),
                        longitude = float(csv_entries[3]) 
                    )   
                    for keyword in csv_entries[4].split(';'):
                        print(keyword)
                        Keywords.objects.create(
                            pois = pois,
                            keyword = keyword
                        )
                    # Create Category objects associated with the PointOfInterest
                    for category in csv_entries[5].split(';'):
                        print(category)
                        Category.objects.create(
                            pois = pois,
                            name = category
                        )
                # Create Keyword objects associated with the PointOfInterest
                    
                    # Serialize the PointOfInterest object 
                    serializer = PointOfInterestSerializer(pois, many = False)
                
                return Response()
            
        except Exception as e:
            print(e)
            return Response({"details": "Error occurred during model creation:"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

