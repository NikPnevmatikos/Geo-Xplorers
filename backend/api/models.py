from django.db import models
from django.contrib.auth.models import User

class PointOfInterest(models.Model):
    #Fields that a location object may contain
    _id = models.AutoField(primary_key=True, editable=False) 

    timestampAdded = models.IntegerField(null=True, blank=True)
    title=models.TextField(max_length=255,null=True, blank=True)
    descritpion=models.TextField(max_length=512,null=True,blank=True)
    latitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)
    longitude=models.DecimalField( max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 
     
    name=models.CharField(max_length=60, null=True, blank=True)
    pois=models.ForeignKey(PointOfInterest,on_delete=models.CASCADE,related_name="categories")
    
    def __str__(self):
        return self.name

class Keywords(models.Model):
    _id = models.AutoField(primary_key=True, editable=False) 

    keyword=models.CharField(max_length=30, null=True, blank=True)
    pois=models.ForeignKey(PointOfInterest,on_delete=models.CASCADE,related_name="keywords")

    def __str__(self):
        return self.keyword


# class Search(models.Model):
#     #The list of available search criteria and optionally their values
#     _id = models.AutoField(primary_key=True, editable=False)
    
    
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    

# class MyUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     subscribed_searches=models.OneToManyField(Search,null=True,blank=True) #User can subscribe to many searches, and one search can in theory be subscribed to by more than one users
#     def __str__(self):
#         return self.user.username
