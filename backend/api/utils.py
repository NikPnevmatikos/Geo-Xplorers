from api.models import PointOfInterest, Category, Keywords
from django.db.models import Q,F
from decimal import Decimal

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
        
    search.temporary_search = False

    search.save()
    return search