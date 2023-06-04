from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework import status, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



# class MyTokenObtainPairSerializer(TokenObtainPairSerializer, TokenObtainSerializer):
    
  
#     # Overiding validate function in the TokenObtainSerializer  
#     def validate(self, attrs):
#         authenticate_kwargs = {
#             'username': attrs['username'],
#             'password': attrs['password'],
#         }
#         try:
#             authenticate_kwargs['request'] = self.context['request']
#         except KeyError:
#             pass

#         # print(f"\nthis is the user of authenticate_kwargs {authenticate_kwargs['email']}\n")
       
        
#         '''
#         Checking if the user exists by getting the email(username field) from authentication_kwargs.
#         If the user exists we check if the user account is active.
#         If the user account is not active we raise the exception and pass the message. 
#         Thus stopping the user from getting authenticated altogether. 
        
#         And if the user does not exist at all we raise an exception with a different error message.
#         Thus stopping the execution righ there.  
#         '''
#         try:
#          user=User.objects.get(username=authenticate_kwargs['username'])
#          if not user.is_active:
#              self.error_messages['no_active_account']=(
#                  'User awaits permission from Admin'
#              )
#              raise exceptions.AuthenticationFailed(
#                  self.error_messages['no_active_account'],
#                  'no_active_account',
#              )
#         except User.DoesNotExist:
#           self.error_messages['no_active_account'] =(
#               'Account does not exist')
#           raise exceptions.AuthenticationFailed(
#               self.error_messages['no_active_account'],
#               'no_active_account',
#           )
          
#         '''
#         We come here if everything above goes well.
#         Here we authenticate the user.
#         The authenticate function return None if the credentials do not match 
#         or the user account is inactive. However here we can safely raise the exception
#         that the credentials did not match as we do all the checks above this point.
#         '''
        
#         self.user = authenticate(**authenticate_kwargs)
#         if self.user is None:
#             self.error_messages['no_active_account'] =(
#                 'Credentials did not match')
#             raise exceptions.AuthenticationFailed(
#                 self.error_messages['no_active_account'],
#                 'no_active_account',
#             )
#         return super().validate(attrs)
    



class User_Serializer(serializers.ModelSerializer):
      
    class Meta:
        model = User
        fields = [
                'first_name',
                'last_name',
                'email',
                'username',
                'is_staff'
                ]
        

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    #if token is decoded the followed information would be shown
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token
    
    #all the json response information for user
    def validate(self, attrs):
        data = super().validate(attrs)
        
        serializer = UserSerializerWithToken(self.user).data
        
        for key, value in serializer.items():
            data[key] = value
            
        
        return data

class UserSerializerWithToken(User_Serializer):

    token = serializers.SerializerMethodField(read_only = True)
    #verified = serializers.BooleanField(source = 'profile.verified')
        
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name',
            'last_name',
            'is_staff', 
            'token', 
        ]
    
    #new access token
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)



#Locations ############################################

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'

class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = '__all__'
class PointOfInterestSerializer(serializers.ModelSerializer): 
    categories = CategorySerializer(many=True) 
    keywords = KeywordsSerializer(many=True)    
    
    class Meta:
        model = PointOfInterest
        fields = '__all__'
class SearchSerializer(serializers.ModelSerializer): 
    categories = CategorySerializer(many=True) 
    keywords = KeywordsSerializer(many=True)    
    

    class Meta:
        model = Search
        fields = '__all__'
        
        