from argparse import ArgumentDefaultsHelpFormatter
import csv
from django.shortcuts import render
from django.contrib.auth.models import User,Search
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
import pandas as pd

class Positions(enum.IntEnum):
    TITLE=0
    DESCRIPTION=1
    LONGITUDE=2
    LATITUDE=3
    KEYWORDS=4
    CATEGORIES=5

    CATEGORY_ID=0
    CATEGORY_NAME=1

MAX_RECENT_SEARCHES=5

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
from .utils import search_point_of_interest

@api_view(['GET'])
def search(request):
    #Get search parameters and return locations matching searc
    #try:
    #    data=request.data
    #    print(data)
    #    if not 'text' in data:
    #        raise ValueError("[text] field is missing")
    #    if not 'filters' in data:
    #        raise ValueError("[filters] field is missing")
    #    filters=data['filters']
    #    if not isinstance(filters,dict):
    #        raise ValueError("[filters] must be a dict")
    #    if not 'categories' in filters:
    #        raise ValueError("[categories] field is missing")
    #    if not isinstance(filters['categories'],list):
    #        raise ValueError("[categories] field must of list type")
    #    if not 'keywords' in filters:
    #        raise ValueError("[keywords] field is missing")
    #    if not isinstance(filters['keywords'],list):
    #        raise ValueError("[keywords] field must of list type")
    #    if not 'distance' in filters:
    #        raise ValueError("[distance] field is missing")
    #    distance=filters['distance']
    #    if not isinstance(distance,dict):
    #        raise ValueError("[filters] must be a dict")
    #    if not 'lng' in distance:
    #        raise ValueError("[lng] field is missing")
    #    if not isinstance(distance['lng'],float):
    #        raise ValueError("[lng] must be a float")
    #    if not 'lat' in distance:
    #        raise ValueError("[lat] field is missing")
    #    if not isinstance(distance['lat'],float):
    #        raise ValueError("[lat] must be a float")
    #    if not 'km' in distance:
    #        raise ValueError("[km] field is missing")
    #    if not isinstance(distance['km'],int):
    #        raise ValueError("[km] must be an int")

        
    #    results = search_point_of_interest(data)

    #    serializer = PointOfInterestSerializer(results,many=True)
    #    print(serializer.data)
    #    return Response({
    #        "start":0,
    #        "count":results.count(),
    #        "total":results.count(),
    #        "data":serializer.data
    #        })
    #except ValueError as e:
    #    return Response({"details":str(e)},status=status.HTTP_400_BAD_REQUEST)
    #except Exception as e:
    #    print(e)
    #    return Response(
    #            {
    #                "details" : "An Error occured during Searching"
    #            },
    #            status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #            )
    try:
        data=request.data
        print(data)
        if not 'text' in data:
            raise ValueError("[text] field is missing")
        if not 'filters' in data:
            raise ValueError("[filters] field is missing")
        filters=data['filters']
        if not isinstance(filters,dict):
            raise ValueError("[filters] must be a dict")
        if not 'categories' in filters:
            raise ValueError("[categories] field is missing")
        if not isinstance(filters['categories'],list):
            raise ValueError("[categories] field must of list type")
        if not 'keywords' in filters:
            raise ValueError("[keywords] field is missing")
        if not isinstance(filters['keywords'],list):
            raise ValueError("[keywords] field must of list type")
        if not 'distance' in filters:
            raise ValueError("[distance] field is missing")
        distance=filters['distance']
        if not isinstance(distance,dict):
            raise ValueError("[filters] must be a dict")
        if len(distance)!=0:
            if ['lat','lng','km'] in distance:
                if not isinstance(distance['lng'],float):
                    raise ValueError("[lng] must be a float")
                if not isinstance(distance['lat'],float):
                    raise ValueError("[lat] must be a float")
                if not isinstance(distance['km'],int):
                    raise ValueError("[km] must be an int")
            else:
                raise ValueError("One or more of the fields [lat,lng,km] is missing from a non empty [distance] array")

        categories=Category.objects.filter(pk__in=data['categories'])
        if categories.count()!=len(data['categories']):
            raise ValueError("Category Id not matching a category in database")
        
        keywords=Keywords.objects.filter(keyword__in=data['keywords'])
        
        
        
        
        search=Search(
            temporary_search=True,
            text=data['text'],
            categories=categories,
            keywords=keywords,
        )
        if request.user.is_authenticated:
            recent_searchs=Search.objects.filter(temporary_search=True).order_by('-timestamp')
            if recent_searchs.count()==MAX_RECENT_SEARCHES:
                recent_searchs.first().delete()
            
            search.user=request.user
            search.timestamp=None
            search.save()
        
        locations=search.findLocations()

        serializer = PointOfInterestSerializer(locations,many=True)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({"details":str(e)},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_all_points(request):
    #Get search parameters and return locations matching search
    pointOfInterest = PointOfInterest.objects.all().order_by('-_id')
    
    serializer = PointOfInterestSerializer(pointOfInterest,many=True)
    
    return Response(serializer.data)

def readFile(upload_file):
    lines=upload_file.read().decode('utf-8').replace('\r','')
    data=[row.split('\t') for row in lines.split('\n')]      
    #print(data)
    return data

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
                if not isinstance(row[Positions.TITLE],str):
                    raise ValueError("Title must be a str: Line "+str(count))
                if not isinstance(row[Positions.DESCRIPTION],str):
                    raise ValueError("Description must be a str: Line "+str(count)) 
                if len(row[Positions.TITLE])==0:
                    raise ValueError("Title cannot be empty: Line "+str(count)) 
                if not isinstance(row[Positions.LONGITUDE],str):
                    raise ValueError("Longitude must be a str: Line "+str(count)) 
                if not isinstance(row[Positions.LATITUDE],str):
                    raise ValueError("Latitude must be a str: Line "+str(count)) 
                if not isinstance(row[Positions.KEYWORDS],str):
                    raise ValueError("Keywords must be a str: Line "+str(count))
                if not isinstance(row[Positions.CATEGORIES],str):
                    raise ValueError("Categories must be a str: Line "+str(count))
                
                categoryIDs=row[Positions.CATEGORIES].split(',')
                categories = Category.objects.filter(id__in = categoryIDs)
                if categories.count()!=len(categoryIDs):
                    raise ValueError("Category Id's do not exist in database: Line "+str(count))


                location = PointOfInterest.objects.create (
                    user = user,
                    title =  row[Positions.TITLE],
                    description = row[Positions.DESCRIPTION],
                    latitude = row[Positions.LONGITUDE],
                    longitude = row[Positions.LATITUDE],
                )   
                for category in categories.all():
                    location.categories.add(category)

                location.save()
                # Create Keyword objects associated with the PointOfInterest
                for keyword in row[Positions.KEYWORDS].split(','):
                    Keywords.objects.create(
                        pois = location,
                        keyword = keyword
                    )
                locations.append(location)

            #check for new data in searches
            for search in Search.objects.filter(temporary_search=False):
                new_data=search.runOptimizedQuery()
                if (len(new_data)!=0):
                    user=search.user
                    #send user an email about said new data of search
            
            serializers = PointOfInterestSerializer(locations, many=True)
            return Response(serializers.data)
    except ValueError as e:
        print(e)
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"details": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def ImportCategories(request):
    try:    
        with transaction.atomic():
            upload_file = request.FILES.get('file')
            if upload_file is None:
                return Response('No file was uploaded.',status=status.HTTP_400_BAD_REQUEST)
            categories = []
            for count,row in enumerate(readFile(upload_file)):
                if len(row)!=2: 
                    raise ValueError("Wrong number of arguments in file, 2 expected: Line "+str(count))
                if not isinstance(row[Positions.CATEGORY_ID],str):
                    raise ValueError("Id must be an int: Line "+str(count))
                if not isinstance(row[Positions.CATEGORY_NAME],str):
                    raise ValueError("Name must be a str: Line "+str(count))
                if len(row[Positions.CATEGORY_NAME])==0:
                    raise ValueError("Name cannot be empty: Line "+str(count))
                
                categoryQuerySet=Category.objects.filter(id=row[Positions.CATEGORY_ID])
                if categoryQuerySet.exists():
                    name=categoryQuerySet.first()
                    if (row[Positions.CATEGORIES]!=name):
                        raise ValueError("Category with Id already exists and is associated with a different name ["+name+"]: Line "+str(count))
                else:
                    item = Category.objects.create(
                        id=int(row[Positions.CATEGORY_ID]),
                        name=row[Positions.CATEGORY_NAME]
                    )
                    categories.append(item)
                    
            serializer = CategorySerializer(categories,many=True)
            return Response(serializer.data)

    except ValueError as e:
        print(e)
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"details": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SearchView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        temporary_search_serializer=SearchSerializer(request.user.searches.filter(temporary_search=True),many=True)
        saved_search_serializer=SearchSerializer(request.user.searches.filter(temporary_search=False),many=True)
        data={
            "recent":temporary_search_serializer.data,
            "saved":saved_search_serializer.data
        }
        return Response(data,status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        try:
            data=request.data
            print(data)
            if not 'text' in data:
                raise ValueError("[text] field is missing")
            if not 'filters' in data:
                raise ValueError("[filters] field is missing")
            filters=data['filters']
            if not isinstance(filters,dict):
                raise ValueError("[filters] must be a dict")
            if not 'categories' in filters:
                raise ValueError("[categories] field is missing")
            if not isinstance(filters['categories'],list):
                raise ValueError("[categories] field must of list type")
            if not 'keywords' in filters:
                raise ValueError("[keywords] field is missing")
            if not isinstance(filters['keywords'],list):
                raise ValueError("[keywords] field must of list type")
            if not 'distance' in filters:
                raise ValueError("[distance] field is missing")
            distance=filters['distance']
            if not isinstance(distance,dict):
                raise ValueError("[filters] must be a dict")
            if len(distance)!=0:
                if ['lat','lng','km'] in distance:
                    if not isinstance(distance['lng'],float):
                        raise ValueError("[lng] must be a float")
                    if not isinstance(distance['lat'],float):
                        raise ValueError("[lat] must be a float")
                    if not isinstance(distance['km'],int):
                        raise ValueError("[km] must be an int")
                else:
                    raise ValueError("One or more of the fields [lat,lng,km] is missing from a non empty [distance] array")

            categories=Category.objects.filter(pk__in=data['categories'])
            if categories.count()!=len(data['categories']):
                raise ValueError("Category Id not matching a category in database")
            
            keywords=Keywords.objects.filter(keyword__in=data['keywords'])
            
            search=models.Search.objects.create(
                timestamp=None,
                temporary_search=False,
                user=request.user,
                text=data['text'],
                categories=categories,
                keywords=keywords,
            )


            serializer = SearchSerializer(search)
            print(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"details":str(e)},status=status.HTTP_400_BAD_REQUEST)
    @permission_classes([IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        data=request.data
        try:
            saved_search=Search.objects.filter(pk=data['_id'])
            if not saved_search.exists():
                raise ValueError("Search matching _id does not exist")
            saved_search.first().delete()

            return Response(status=status.HTTP_202_ACCEPTED)
        except ValueError as e:
            return Response({"details":str(e)},status=status.HTTP_400_BAD_REQUEST)
