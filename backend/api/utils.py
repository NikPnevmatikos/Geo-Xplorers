from api.models import PointOfInterest, Category, Keywords
from django.db.models import Q


def search_point_of_interest(data):
    # Search logic here

    filters = data['filters']

    categories = Category.objects.filter(id__in = filters['categories'])
    keywords = Keywords.objects.filter(keyword__in = filters['keywords'])

    distance = filters['distance']

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
    queryset = PointOfInterest.objects.filter(query)

    return queryset