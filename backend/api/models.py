import datetime
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q,F
#from django.contrib.gis.geos import Point

class Category(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 
     
    id=models.IntegerField(null=True, blank=True)
    name=models.CharField(max_length=60, null=True, blank=True)
    #pois=models.ForeignKey(PointOfInterest,null=True,on_delete=models.CASCADE,related_name="categories")
    
    def __str__(self):
        return self.name

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

    categories = models.ManyToManyField(Category,related_name="categories", blank=True)

    
    def __str__(self):
        return self.title


class Keywords(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 

    keyword=models.CharField(max_length=30, null=True, blank=True)
    pois=models.ForeignKey(PointOfInterest,on_delete=models.CASCADE,related_name="keywords")

    def __str__(self):
        return self.keyword


class Search(models.Model):
   #The list of available search criteria and optionally their values
    _id = models.AutoField(primary_key=True, editable=False)

    timestamp=models.DateTimeField()
    temporary_search=models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="searches")
    text=models.TextField(max_length=512,null=True,blank=True)
    categories=models.ManyToManyField(Category,related_name="searches")
    keywords=models.ManyToManyField(Keywords,related_name="searches")
    latitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)
    longitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)
    kilometers=models.IntegerField()

    cache_locations=models.ManyToManyField(PointOfInterest,related_name="searches")

    def runOptimizedQuery(self):
        query = Q()
        if not self.temporary_search and self.timestamp is not None:
            query.add(Q(timestamp__gt=self.timestamp),Q.AND)
        if self.text != '':
            query.add(Q(title__contains = self.text), Q.OR)
            query.add(Q(description__contains = self.text), Q.OR)

        if self.categories.count() > 0:
            query.add(Q(categories__in=self.categories), Q.AND)
        elif self.text != '':
            query.add(Q(categories__name__contains=self.text), Q.OR)

        if self.keywords.count() > 0:
            query.add(Q(keywords__in=self.keywords), Q.AND)
        elif self.text != '':
            query.add(Q(keywords__keyword__contains=self.text), Q.OR)

        transaformedPois=PointOfInterest.objects.annotate(
            radius_sqr=pow(F('latitude') - Decimal(self.latitude), Decimal(2)) + 
                    pow(F('longitude') - Decimal(self.longitude), Decimal(2))
        )
        query.add(Q(radius_sqr__lte=pow(self.kilometers*1000, 2)), Q.AND)
        

        queryset = transaformedPois.filter(query)
        if not self.temporary_search:
            self.timestamp=datetime.datetime.now()
            for location in queryset.all():
                self.cache_locations.add(location)
            self.save()
        return queryset.all()
    
    def findLocations(self):
        locations=self.cached_locations.all()
        for new_location in self.runOptimizedQuery():
            locations.append(new_location)
        return locations
