from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q,F
from django.utils import timezone
#from django.contrib.gis.geos import Point

class Category(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 
     
    id=models.IntegerField(null=True, blank=True)
    name=models.CharField(max_length=60, null=True, blank=True)
    #pois=models.ForeignKey(PointOfInterest,null=True,on_delete=models.CASCADE,related_name="categories")
    
    def __str__(self):
        return self.name

class Keywords(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 

    keyword=models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.keyword
    
class PointOfInterest(models.Model):
    #Fields that a location object may contain
    _id = models.AutoField(primary_key=True, editable=False) 

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    timestampAdded = models.DateTimeField(auto_now_add=True)
    title=models.TextField(max_length=255,null=True, blank=True)
    description=models.TextField(max_length=512,null=True,blank=True)
    latitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)
    longitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)
    #point = models.PointField(blank=True, null=True)

    categories = models.ManyToManyField(Category,related_name="locations")
    keywords=models.ManyToManyField(Keywords,related_name="locations")
    
    def __str__(self):
        return self.title





class Search(models.Model):
   #The list of available search criteria and optionally their values
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
    #
    def __runOptimizedQuery(self,timestamp):
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
        locations=[location for location in self.cache_locations.all()]
        print(locations,"Old \n\n")        

        new_locations=self.__runOptimizedQuery(self.timestamp)    
        print(new_locations,"New \n\n") 
        self.timestamp=timezone.localtime()
        for new_location in new_locations:
            self.cache_locations.add(new_location)
            locations.append(new_location)
        
        self.save()
        
        return locations
        
    def findNewData(self,import_timestamp):
        return self.__runOptimizedQuery(import_timestamp)
    

class Announcement(models.Model):
    # {image, message ,detailPage, receivedTime}
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True, default='/MapIcon.png')
    message = models.CharField(max_length=200, null=True, blank=True)
    detailPage = models.CharField(max_length=200, null=True, blank=True, default='http://localhost:3000/')
    receivedTime = models.DateTimeField(auto_now_add=True)
    
    _id = models.AutoField(primary_key=True, editable=False)
    
    
    def __str__(self):
        return self.message
