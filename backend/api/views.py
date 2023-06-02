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
import enum 

class Positions(enum.IntEnum):
    TITLE=0
    DESCRIPTION=1
    LONGITUDE=2
    LATITUDE=3
    KEYWORDS=4
    CATEGORIES=5

    CATEGORY_ID=0
    CATEGORY_NAME=1



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


def readFile(upload_file):
    lines=upload_file.read().decode('utf-8').replace('\r','')
    data=[]
    for row in lines.split('\n'):
        data.append([element for element in row.split(',')])        
    return data
        

# defines a view for creating and retrieving PointOfInterest objects with
# associated Category and Keyword objects.


@api_view(['GET'])
def get_all_points(request):
    #Get search parameters and return locations matching search
    pointOfInterest = PointOfInterest.objects.all().order_by('-_id')
    
    serializer = PointOfInterestSerializer(pointOfInterest,many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def ImportLocations(request):
    """
    This is a view function that creates a new PointOfInterest object with associated Category and
    Keyword objects, and returns a serialized representation of the created object.
    
    """
    try:    
        with transaction.atomic():
            user = request.user
            #this will change because the request.data will have the file containing this data
            upload_file = request.FILES.get('file')
            if upload_file is None:
                return Response('No file was uploaded.',status=status.HTTP_400_BAD_REQUEST)
            locations=[]
            for count,row in enumerate(readFile(upload_file)):
                # Create a new PointOfInterest object with the provided data
                if len(row)!=6:
                    raise ValueError("Wrong number of arguments in file, 6 expected: Line "+str(count))
                if len(row[Positions.TITLE])==0:
                    raise ValueError("Title is mandatory: Line "+str(count)) 

                if not row[Positions.LONGITUDE].replace('.','').isdigit():
                    raise ValueError("Longitude must be a decimal: Line "+str(count)) 
                if not row[Positions.LATITUDE].replace('.','').isdigit():
                    raise ValueError("Latitude must be a decimal: Line "+str(count)) 

                categories = Category.objects.filter(id__in = row[Positions.CATEGORIES].split(';'))


                location = PointOfInterest.objects.create (
                    user = user,
                    title =  row[Positions.TITLE],
                    description = row[Positions.DESCRIPTION],
                    latitude = float(row[Positions.LONGITUDE]),
                    longitude = float(row[Positions.LATITUDE]),
                )   
                for category in categories.all():
                    location.categories.add(category)

                location.save()
                # Create Keyword objects associated with the PointOfInterest

                for keyword in row[Positions.KEYWORDS].split(';'):
                    print(keyword,"Key")
                    Keywords.objects.create(
                        pois = location,
                        keyword = keyword
                    )
                locations.append(location)

            serializers = PointOfInterestSerializer(locations, many=True)
            return Response(serializers.data)
    except ValueError as e:
        print(e)
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"details": "Error occurred during model creation:"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def ImportCategories(request):
    try:    
        with transaction.atomic():
            #this will change because the request.data will have the file containing this data
            upload_file = request.FILES.get('file')
            if upload_file is None:
                return Response('No file was uploaded.',status=status.HTTP_400_BAD_REQUEST)
            categories = []
            for count,category in enumerate(readFile(upload_file)):
                if len(category)!=2: 
                    raise ValueError("Wrong number of arguments in file, 2 expected: Line "+str(count))
                if len(category[Positions.CATEGORY_NAME])==0:
                    raise ValueError("Name cannot be empty: Line "+str(count))
                if len(category[Positions.CATEGORY_ID])==0:
                    raise ValueError("Id cannot be empty: Line "+str(count))
                if not category[Positions.CATEGORY_ID].isdigit():
                    raise ValueError("Id must be an integer: Line "+str(count))
                
                
                item = Category.objects.create(
                    id=int(category[Positions.CATEGORY_ID]),
                    name=category[Positions.CATEGORY_NAME]
                )
                categories.append(item)
                    
            serializer = CategorySerializer(categories,many=True)
            return Response(serializer.data)

    except ValueError as e:
        print(e)
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"details": "Error occurred during model creation:"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SearchView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        #Get all searchs that the user is subscribed to
        pass
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        #same logic as POST api/search/location but instead of calling findMatchingLocations(), we save the search Object
        pass
    @permission_classes([IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        #Remove search the search from saved searches
        pass

# class SearchLocationView(APIView):
    
#     def post(self, request, *args, **kwargs):
#         try:    
#             data=request.data
#             #something something to link categories and keywords to search
#             #....
            
#             search=Search(
#                 text=data['text']    
#                 #...
#             )
#             locations=search.findMatchingLocations()
#             return Response(locations)
#         except Exception as e:
#             print(e)
#             return Response({"details": "Error occurred during model creation:"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
