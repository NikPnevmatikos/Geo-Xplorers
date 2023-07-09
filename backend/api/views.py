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

MAX_RECENT_SEARCHES=5

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer    

# The class MyUserView is an API view that allows for creating and retrieving user information.
class MyUserView(APIView):

    def post(self,request,*args,**kwargs):
        """
        The above function creates a new user with the provided data and returns a response with the
        serialized user data, or an error message if there is already an account with the same email or
        username.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by
        the client. It contains information such as the request method (GET, POST, etc.), headers, body,
        and query parameters
        :return: The code is returning a response with the serialized data of the created user if the
        user creation is successful. If there is an exception, it returns a response with a message
        indicating that there is already an account using the provided email or username.
        """
        data = request.data
        try:

            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                username = data['username'], 
                email = data['email'],
                password = make_password(data['password'])
            )

            serializer = UserSerializerWithToken(user, many = False)
            
            return Response(serializer.data)
        except Exception as e: 
            message = {'detail' : 'There is already an account using this email or username.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        """
        This function checks if the user is authenticated and returns the serialized data of the user if
        they are authenticated.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by
        the client. It contains information such as the request method (GET, POST, etc.), headers, query
        parameters, and the body of the request
        :return: The code is returning a response with the serialized data of the authenticated user.
        """
        if not request.user.is_authenticated:
            return Response({"details":"Authentication credentials were not provided."},status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        

        serializer = User_Serializer(user)
        return Response(serializer.data)




from .utils import search_point_of_interest,addToSaved

@api_view(['POST'])
def search(request):
    """
    The `search` function takes a request and performs a search based on the provided data, returning a
    response with the matching locations.
    
    :param request: The `request` parameter is an object that contains information about the HTTP
    request made to the server. It includes data such as the request method (GET, POST, etc.), headers,
    query parameters, and the request body
    :return: a Response object with a JSON payload. The JSON payload includes the following fields:
    - "_id": The ID of the search.
    - "start": The starting index of the search results.
    - "count": The number of search results returned.
    - "total": The total number of search results available.
    - "data": An array of search results, serialized using the PointOf
    """

    data=request.data
    search_id=request.query_params.get('pk')

    with transaction.atomic():
        try:
            if search_id is not None and request.user.is_authenticated:
                search=request.user.searches.filter(pk=search_id)
                if search.exists():
                    locations=search.first().findMatchingLocations()
                    serializer=PointOfInterestSerializer(locations,many=True)
                    return Response({
                        "_id" : search.first()._id,
                        "start" : 0,
                        "count" : len(serializer.data),
                        "total" : len(serializer.data),
                        "data" :serializer.data
                    },status=status.HTTP_200_OK)
                else:
                    raise ValueError("No saved or recent search with id: "+str(search_id)+" exists")
            else:
                if not 'text' in data:
                    raise ValueError("[text] field is missing")
                if not 'filters' in data:
                    raise ValueError("[filters] field is missing")
                filters=data['filters']
                if not isinstance(filters,dict):
                    raise ValueError("[filters] must be a dict")
                if not 'categories' in filters:
                    raise ValueError("[categories] field is missing")
                categories_list=filters['categories']
                if not isinstance(filters['categories'],list):
                    raise ValueError("[categories] field must of list type")
                if not 'keywords' in filters:
                    raise ValueError("[keywords] field is missing")
                if not isinstance(filters['keywords'],list):
                    raise ValueError("[keywords] field must of list type")
                if not 'distance' in filters:
                    raise ValueError("[distance] field is missing")
                distance=filters.get('distance',None)
                if not isinstance(distance,dict):
                    raise ValueError("[filters] must be a dict")
                longitude=distance.get('lng',None)
                latitude=distance.get('lat',None)
                kilometers=distance.get('km',None)
                if len(distance)!=0:
                    if (longitude is not None) and (latitude is not None) and (kilometers is not None):
                        if not isinstance(longitude,float):
                            raise ValueError("[lng] must be a float")
                        if not isinstance(latitude,float):
                            raise ValueError("[lat] must be a float")
                        if not isinstance(kilometers,int):
                            raise ValueError("[km] must be an int")
                    else:
                        raise ValueError("One or more of the fields [lat,lng,km] is missing from a non empty [distance] array")

                categories=Category.objects.filter(id__in=categories_list)
                if categories.count()!=len(categories_list):
                    raise ValueError("Input category not matching a category in database")
                
                user=None
                if request.user.is_authenticated:
                    user=request.user
                
                search=Search.objects.create(
                    user=user,
                    timestamp=None,
                    subscribed_search=False,
                    text=data['text'],
                    longitude=longitude,
                    latitude=latitude,
                    kilometers=kilometers
                )
        
                for category in categories.all():
                    search.categories.add(category)
                
                for keyword in filters['keywords']:
                    keyword_query=Keywords.objects.filter(keyword=keyword)
                    if not keyword_query.exists():
                        keyword_obj=Keywords.objects.create(
                            keyword = keyword
                        )
                    else:
                        keyword_obj=keyword_query.first()
                    search.keywords.add(keyword_obj)
                
                search.save()

                locations=search.findMatchingLocations()
                
                if not request.user.is_authenticated:
                    search.delete()
                
                start=0
                count=len(locations)
                if ('start' in data) and ('count' in data):
                    start=data['start']
                    count=data['count']
                    end=count+start
                    if (start>=len(locations) or end>len(locations) or start<0 or end<0):
                        raise ValueError("[start] and [count] parameters exceed results range")
                    locations=locations[start:end]
                    
                serializer = PointOfInterestSerializer(locations,many=True)
                return Response({
                    "_id" : search._id,
                    "start" : start,
                    "count" : count,
                    "total" : len(serializer.data),
                    "data" :serializer.data
                    
                    },status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"details":str(e)},status=status.HTTP_400_BAD_REQUEST)


import base64

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request, pk):
    """
    The `upload_image` function takes a request and a primary key as input, decodes an image from the
    request data, saves it to a file, and associates it with a search object.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method, headers, and data
    :param pk: The "pk" parameter is the primary key of the Search object that we want to associate the
    uploaded image with. It is used to retrieve the specific Search object from the database
    :return: a Response object. If the image is successfully saved, it will return a response with the
    message "Image Saved". If an error occurs, it will return a response with the message "Error
    occurred" and a status code of 500.
    """
    try:
        search = Search.objects.get(_id=pk)
        #write the decoded data back to original format in  file
        format, imgstr = request.data['image'].split(';base64,') 
        ext = format.split('/')[-1] 
        decoded_data=base64.b64decode((imgstr))
        img_file = open(f'./static/images/Temp.{ext}', 'wb+')
        img_file.write(decoded_data)
        search.image.save(f'{search._id}.{ext}', img_file, save=False)
        img_file.close()
        search.save()
        
        
        return Response({"details" : "Image Saved"})
    except Exception as e:
        return Response({"details": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_all_points(request):
    #Get search parameters and return locations matching search
    pointOfInterest = PointOfInterest.objects.all().order_by('-_id')
    
    serializer = PointOfInterestSerializer(pointOfInterest,many=True)

    return Response(serializer.data)

def readFile(upload_file):
    """
    The function `readFile` reads the contents of an uploaded file, decodes it using UTF-8 encoding,
    removes any carriage return characters, splits the contents into lines, and then splits each line
    into a list of values separated by tabs.
    
    :param upload_file: The parameter `upload_file` is expected to be a file object that is opened in
    binary mode. It should be a file that you want to read and process
    :return: a list of lists, where each inner list represents a row of data from the uploaded file.
    """
    lines=upload_file.read().decode('utf-8').replace('\r','')
    data=[row.split('\t') for row in lines.split('\n')]      
    return data

from .utils import send_email, send_lot_email

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
            import_timestamp=timezone.localtime()
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
                for id in categoryIDs:
                    if (id==""):
                        raise ValueError("Incorrect format for categories list")
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
                    if (keyword==""):
                        raise ValueError("Incorrect format for keywords list")
                    keyword_query=Keywords.objects.filter(keyword=keyword)
                    if not keyword_query.exists():
                        keyword_obj=Keywords.objects.create(
                            keyword = keyword
                        )
                    else:
                        keyword_obj=keyword_query.first()
                    location.keywords.add(keyword_obj)
                
                locations.append(location)

            #check for new data in searches
            recipient_list = []
            for search in Search.objects.filter(subscribed_search=True):
                new_data=search.findNewData(import_timestamp)
                if (len(new_data)!=0):
                    
                    announcement = Announcement.objects.create(
                        user = search.user,
                        message = str(len(new_data)) + ' new points in your search'
                    )
                    
                    search.newPois = len(new_data)
                    search.save()
                    
                    categories_list = [category.name for category in search.categories.all()]
                    keywords_list = [keyword.keyword for keyword in search.keywords.all()]
                    recipient = {
                                    'email': search.user.email,
                                    'name': search.user.first_name + " " + search.user.last_name,
                                    'new_locations': str(len(new_data)),
                                    'search': 
                                        {
                                            "filters" :{
                                                "categories": categories_list,
                                                "keywords": keywords_list,
                                                "distance": {'lat':str(search.latitude),'lng':str(search.longitude),'km':str(search.kilometers)}
                                            },
                                            "text": search.text

                                        }                
                                }
                                
                    #email=search.user.email
                    recipient_list.append(recipient)
                    #send user an email about said new data of search
                    
            
            #send_email(recipient_list)
            send_lot_email(recipient_list)
            
            serializers = PointOfInterestSerializer(locations, many=True)
            return Response(serializers.data)
    except ValueError as e:
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"details": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def ImportCategories(request):
    """
    The function `ImportCategories` imports categories from a file and saves them in the database,
    returning a response with the serialized data.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method, headers, and body. In this case, it is
    used to retrieve the uploaded file from the request body using `request.FILES.get('file')`
    :return: a Response object. The specific response depends on the execution path of the code. If
    there are no errors, it returns a Response object with the serialized data of the created
    categories. If there is a ValueError, it returns a Response object with the details of the error and
    a status code of 400 (Bad Request). If there is any other exception, it returns a Response object
    """
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
                    name=categoryQuerySet.first().name
                    if (row[Positions.CATEGORY_NAME]!=name):
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
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"details": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def GetCategories(request):
    """
    The function `GetCategories` retrieves all categories from the database and returns them as a
    serialized response.
    """
    try:
        categories = Category.objects.all().order_by('-_id')
        
        serializer = CategorySerializer(categories,many=True)
        
        return Response(serializer.data)
        
    except Exception as e:
        return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

@permission_classes([IsAuthenticated])
class SearchView(APIView):
    def get(self, request, *args, **kwargs):  
        try:
            type=request.query_params.get('type',None)
            if type is None:
                raise ValueError('[type] field missing')
            if type not in ['saved','recent']:
                raise ValueError('[type] must be either \"recent\" or \"saved\"')

            if type=="recent":
                serializer=SearchSerializer(request.user.searches.filter(subscribed_search=False).order_by('-timestamp')[:(MAX_RECENT_SEARCHES)],many=True)
            elif type=="saved":
                serializer=SearchSerializer(request.user.searches.filter(subscribed_search=True).order_by('-timestamp'),many=True)
            else:
                raise ValueError('[type] must be either \"recent\" or \"saved\"')

            return Response(serializer.data,status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"details":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, *args, **kwargs):
        try:
            search_id=request.query_params.get('pk')
            if search_id is None:
                raise ValueError("[_id] field is missing")
            
            search_query=request.user.searches.filter(_id=search_id)
            if not search_query.exists():
                raise ValueError("Search matching _id: "+str(search_id)+" does not exist")
            search=search_query.first()
            if search.subscribed_search:
                raise ValueError("Cannot subscribe to an already Subscribed Search")
            

            new_search=addToSaved(search)

            serializer=SearchSerializer(new_search)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"details":str(e)},status=status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, *args, **kwargs):
        try:
            id=request.query_params.get('pk',None)
            if id is None:
                raise ValueError("[_id] field is missing")
            saved_search=request.user.searches.filter(pk=id)
            if not saved_search.exists():
                raise ValueError("Search matching _id "+str(id)+" does not exist")
            saved_search.first().delete()

            return Response({"Status" : "OK" },status=status.HTTP_202_ACCEPTED)
        except ValueError as e:
            return Response({"details":str(e)},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_announcements(request):
    user = request.user
    
    announcement = Announcement.objects.filter(user=user)
    
    serializer = AnnouncementSerializer(announcement,many = True)
    
    return Response(serializer.data)