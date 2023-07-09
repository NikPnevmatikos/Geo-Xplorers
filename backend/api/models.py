from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.utils import timezone

class Category(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 
     
    id=models.IntegerField(null=True, blank=True)
    name=models.CharField(max_length=60, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Keywords(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 

    keyword=models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.keyword
    
class PointOfInterest(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    timestampAdded = models.DateTimeField(auto_now_add=True)
    title=models.TextField(max_length=255,null=True, blank=True)
    description=models.TextField(max_length=512,null=True,blank=True)
    latitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)
    longitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)
    categories = models.ManyToManyField(Category,related_name="locations")
    keywords=models.ManyToManyField(Keywords,related_name="locations")
    
    def __str__(self):
        return self.title





class Search(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)

    image = models.ImageField(null=True, blank=True, default='/defaultMap.png')
    timestamp=models.DateTimeField(null=True, blank=True)
    subscribed_search=models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="searches")
    text=models.TextField(max_length=512,null=True,blank=True)
    categories=models.ManyToManyField(Category,related_name="searches")
    keywords=models.ManyToManyField(Keywords,related_name="searches")
    latitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)
    longitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)
    kilometers=models.IntegerField(null=True,blank=True)
    cache_locations=models.ManyToManyField(PointOfInterest,related_name="searches")
    newPois = models.IntegerField(null=True,blank=True, default=0)


    def __str__(self):
        return self.text + " " + str(self._id) 
    
    def __runOptimizedQuery(self,timestamp):
        """
        The function `__runOptimizedQuery` is used to run an optimized query on a database to retrieve a
        set of PointOfInterest objects based on various filters such as timestamp, text, categories,
        keywords, latitude, longitude, and kilometers.
        
        :param timestamp: The `timestamp` parameter is used to filter the results based on the
        `timestampAdded` field. It retrieves all records with a `timestampAdded` greater than the
        provided `timestamp`
        :return: a queryset of PointOfInterest objects that match the specified conditions in the query.


        Exact details on how the search logic functions are explained below:
            If all of “latitude”, “longitude”, “kilometers” parameters exist then the results will be limited by whether or not the point of interest is inside the circle defined by the parameters.
            If the “categories” parameter is present, then a location will be included in the final result only if at least one of it's categories matches the input category list
            Likewise for the “keywords” parameter, if it is present, then a location will be included in the final result only if at least one of it's keywords matches the input keyword list
            If the “text” parameter is present, it is always applied to the “title” and “description” attributes of the locations, and a location must also satisfy either one of the above to be of match.
                In the case that no input categories have been given, then the “text” parameter is also applied to the categories.
                Similarly for when the input keywords is missing, the “text” is applied to the keywords attribute
                The previous two mean that in the event that no categories and no keywords are present, the “text” parameter can satisfy either one of the “title”,“description”,”categories”,”keywords” attributes of the location.
                The matching for the “text” parameter works with by whether or not the attribute we match against contains a substring matching the “text” 
                i.e If one location has “title”:”Lake Dunmore” and another has “categories”:[“big lakes”,...] then both will match the “text”:”lake” input parameter.

        """
        query = Q()
        if timestamp is not None:
            query=(Q(timestampAdded__gt=timestamp))
        
        free_text_filter=Q()
        if self.text != '':
            free_text_filter.add(Q(title__contains = self.text), Q.OR)
            free_text_filter.add(Q(description__contains = self.text), Q.OR)
        
        if self.categories.count() > 0:
            query.add(Q(categories__in=self.categories.all()),Q.AND)
        elif self.text != '':
            free_text_filter.add(Q(categories__name__contains=self.text), Q.OR)

        if self.keywords.count() > 0:
            query.add(Q(keywords__in=self.keywords.all()), Q.AND)
        elif self.text != '':
            free_text_filter.add(Q(keywords__keyword__contains=self.text), Q.OR)

        query.add(free_text_filter,Q.AND)

        if self.latitude and self.longitude and self.kilometers:
            transaformedPois=PointOfInterest.objects.annotate(
                radius_sqr=pow(F('latitude') - Decimal(self.latitude), Decimal(2)) + 
                        pow(F('longitude') - Decimal(self.longitude), Decimal(2))
            )
            query.add(Q(radius_sqr__lte=pow(self.kilometers*1000, 2)), Q.AND)

            queryset = transaformedPois.filter(query).distinct().order_by('-_id')
            
        else:
            queryset = PointOfInterest.objects.filter(query).distinct().order_by('-_id')


        return queryset.all()
    
    def findMatchingLocations(self):
        """
        The function "findMatchingLocations" retrieves a list of locations from a cache, runs an
        optimized query to get new locations, adds the new locations to the cache, updates the
        timestamp, saves the changes, and returns the combined list of locations.
        :return: a list of locations.
        """
        #locations=[location for location in self.cache_locations.all()]       
        #new_locations=self.__runOptimizedQuery(None)    
        #self.timestamp=timezone.localtime()
        #for new_location in new_locations:
        #    self.cache_locations.add(new_location)
        #    locations.append(new_location)
        locations=self.__runOptimizedQuery(None);    
        
        self.newPois = 0
        self.save()
        
        return locations
        
    def findNewData(self,import_timestamp):
        """
        The function "findNewData" returns the result of running an optimized query using the given
        import timestamp.
        
        :param import_timestamp: The import_timestamp parameter is a timestamp that represents the time
        at which the data was imported. It is used as a reference point to find new data that has been
        imported after this timestamp
        :return: the result of the `__runOptimizedQuery` method.
        """
        return self.__runOptimizedQuery(import_timestamp)
    

class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True, default='/MapIcon.png')
    message = models.CharField(max_length=200, null=True, blank=True)
    detailPage = models.CharField(max_length=200, null=True, blank=True, default='http://localhost:3000/')
    receivedTime = models.DateTimeField(auto_now_add=True)
    
    _id = models.AutoField(primary_key=True, editable=False)
    
    
    def __str__(self):
        return self.message
