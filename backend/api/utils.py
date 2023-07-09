from api.models import PointOfInterest, Category, Keywords
from django.db.models import Q,F
from decimal import Decimal

#TODO remove old search function
def search_point_of_interest(data):
    # Search logic here

    filters = data['filters']

    categories = Category.objects.filter(id__in = filters['categories'])
    keywords = Keywords.objects.filter(keyword__in = filters['keywords'])

    distance = filters['distance']
    radius=distance['km']
    latitude=distance['lat']
    longitude=distance['lng']

    query = Q()
    if data['text'] != '':
        query.add(Q(title__contains = data['text']), Q.OR)
        query.add(Q(description__contains = data['text']), Q.OR)

    if len(filters['categories']) > 0:
        query.add(Q(categories__in=categories), Q.AND)
    elif data['text'] != '':
        query.add(Q(categories__name__contains=data['text']), Q.OR)

    if len(filters['keywords']) > 0:
        query.add(Q(keywords__in=keywords), Q.AND)
    elif data['text'] != 0:
        query.add(Q(keywords__keyword__contains=data['text']), Q.OR)


    # latituderange=(latitude - distance, latitude + distance),
    #                               longituderange=(longitude - distance, longitude + distance
    #query.add(Q(latitude__range = (distance['lat'] - distance, distance['lat'] + distance)), Q.AND)
    #query.add(Q(longitude__range = (distance['lng'] - distance, distance['lng'] + distance)), Q.AND)
    transaformedPois=PointOfInterest.objects.annotate(
        radius_sqr=pow(F('latitude') - Decimal(latitude), Decimal(2)) + 
                pow(F('longitude') - Decimal(longitude), Decimal(2))
    )
    query.add(Q(radius_sqr__lte=pow(radius*1000, 2)), Q.AND)
    queryset = transaformedPois.filter(query)

    #queryset = PointOfInterest

    return queryset


def addToSaved(search):
    """
    The function addToSaved takes a search object, saves it with a new id, adds categories, keywords,
    and cache locations to the search object, sets subscribed_search to True, and saves the search
    object again before returning it.
    
    :param search: The "search" parameter is an object that represents a search query. It has the
    following attributes:
    :return: the "search" object after it has been modified and saved.
    """
    categories = search.categories
    keywords = search.keywords
    cache_locations = search.cache_locations

    search._id=None
    search.save()
    print(search,' after id save')
    for category in categories.all():
        search.categories.add(category)
    for keyword in keywords.all():
        search.keywords.add(keyword)
    for cache_location in cache_locations.all():
        search.cache_locations.add(cache_location)
        
    search.subscribed_search = True

    search.save()
    return search


from django.core.mail import EmailMessage, get_connection, send_mass_mail
from django.conf import settings

def send_email(receivers):   
    with get_connection(  
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = 'new data imported'
        email_from = settings.EMAIL_HOST_USER  
        recipient_list = receivers 
        message = 'dear costumer, one of your save searches has new data. Check it out'  
        EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()  
        

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_lot_email(recipients):
        """
        The function `send_lot_email` sends an email to each recipient with information about new points of
        interest that match their search criteria.
        
        :param recipients: A list of dictionaries, where each dictionary represents a recipient and contains
        the following keys:
        """
        
        subject = 'Stay in the Loop: New Points of Interest Match Your Search Criteria!'
        
        # 'search': {
        #                 "filters" :{
        #                     "categories": ['lake', 'balls'],
        #                     "keywords": ['keyword3','keyword2'],
        #                     "distance": {'lat':'0.0','lng':'0.0','km':'25'}
        #                 },
        #                 "text": "testdfhbkjdfbbkjk"

        #             }  

    
        for recipient in recipients:
            search = recipient['search']
            filters = search['filters']
            distance = filters['distance']
            context = {
                'name': recipient['name'],
                'new_locations' : recipient['new_locations'],
                'text': search['text'],
                'categories': filters['categories'],
                'keywords': filters['keywords'],
                'lat': distance['lat'],
                'lng': distance['lng'],
                'km': distance['km']
            }
            
            message = render_to_string('emailNotificationTemplate.html', context)

            plain_message = strip_tags(message)
            from_email = settings.EMAIL_HOST_USER
            recipient_email = recipient['email']

            email = EmailMultiAlternatives(subject, plain_message, from_email, [recipient_email])
            email.attach_alternative(message, 'text/html')
            email.content_subtype = 'html'
            
            email.send()
            
            #email_data.append((email.subject, email.body, email.from_email, email.to , ))
            #email_data.append(email)
        
        #send_mass_mail(email_data, fail_silently=False)
            
        #send_mass_mail(email_data, fail_silently=False)