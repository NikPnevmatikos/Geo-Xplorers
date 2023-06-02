from django.db import models
from django.contrib.auth.models import User

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
    categories = models.ManyToManyField(Category,related_name="categories", blank=True)
    
    def __str__(self):
        return self.title


class Keywords(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 

    keyword=models.CharField(max_length=30, null=True, blank=True)
    pois=models.ForeignKey(PointOfInterest,on_delete=models.CASCADE,related_name="keywords")

    def __str__(self):
        return self.keyword


# class Save_seacr(models.Model):
#    #The list of available search criteria and optionally their values
#     _id = models.AutoField(primary_key=True, editable=False)

#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     text=models.TextField(max_length=512,null=True,blank=True)
#     categories=models.ManyToManyField(Category,on_delete=models.CASCADE,related_name="searches")
#     keywords=models.ManyToManyField(Keywords,on_delete=models.CASCADE,related_name="searches")

#     def findMatchingLocations():
#         locations=[]
#         #find all locations matching search criteria
#         return locations
