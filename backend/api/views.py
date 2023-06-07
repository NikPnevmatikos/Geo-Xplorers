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
from .utils import search_point_of_interest,addToSaved

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
    data=request.data
    search_id=request.query_params.get('pk')

    with transaction.atomic():
        try:
            if search_id is not None and request.user.is_authenticated:
                search=request.user.searches.filter(pk=search_id)
                if search.exists():
                    locations=search.first().findMatchingLocations()
                    serializer=PointOfInterestSerializer(locations,many=True)
                    print(serializer.data)
                    return Response(serializer.data,status=status.HTTP_200_OK)
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

                categories=Category.objects.filter(name__in=categories_list)
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

                #if request.user.is_authenticated:
                #    recent_searches=Search.objects.filter(temporary_search=True).order_by('timestamp')
                #    if recent_searches.count()==MAX_RECENT_SEARCHES+1:
                #        recent_searches.first().delete()
                
                if not request.user.is_authenticated:
                    search.delete()
                
                print(locations, '\n\n\n\n\n\n\n')
                
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

@permission_classes([IsAuthenticated])
class SearchView(APIView):
    def get(self, request, *args, **kwargs):        
        recent_search_serializer=SearchSerializer(request.user.searches.all().order_by('-timestamp')[:(MAX_RECENT_SEARCHES)],many=True)
        subscribed_search_serializer=SearchSerializer(request.user.searches.filter(subscribed_search=True).order_by('-timestamp'),many=True)
        
        
        data={
            "recent":recent_search_serializer.data,
            "saved":subscribed_search_serializer.data
        }
        print(data)
        return Response(data,status=status.HTTP_200_OK)
        
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
            

            search.subscribed_search=True
            search.save()

            serializer=SearchSerializer(search)
            print(serializer.data)
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
        
from .utils import send_lot_email

@api_view(['POST'])
def send_email_to_users(request):
    try:
        recipients = [
            {
                'email': 'nikpnevmatikos@gmail.com',
                'name': 'Nick the greek',
                'new_locations': '3',
                'search': {
                        "filters" :{
                            "categories": ['lake', 'house'],
                            "keywords": ['keyword'],
                            "distance": {'lat':'0.0','lng':'0.0','km':'25'}
                        },
                        "text": "test"

                    }                
            },
            {
                'email': 'tikonikos@gmail.com', 
                'name': 'God Nicky nicky',
                'new_locations': '10',
                'search': {
                        "filters" :{
                            "categories": ['lake', 'balls'],
                            "keywords": ['keyword3','keyword2'],
                            "distance": {'lat':'0.0','lng':'0.0','km':'25'}
                        },
                        "text": "testdfhbkjdfbbkjk"

                    }  
            },
        ]
        
        send_lot_email(recipients)
        #send_mass_mail(email_data, fail_silently=False)
        return Response({"details": "Email Send"})
    except Exception as e:
        print(e)
        return Response({"details": "Something went wrong"})
