from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenRefreshView,TokenObtainPairView


urlpatterns = [
   path('login/', views.MyTokenObtainPairView.as_view(), ),
   path('user/', views.MyUserView.as_view()),
   path('import/categories/',views.ImportCategories),
   path('import/pois/',views.ImportLocations),
   path('token/refresh/', TokenRefreshView.as_view()),
   path('search/pois/',views.search),
   #path('search/pois/<str:pk>/',views.search),
   path('searches/',views.SearchView.as_view()),
   
   path('get/pois/', views.get_all_points),
   
   path('categories/', views.GetCategories),
   path('search/image/<str:pk>/', views.upload_image),
   path("announcement/", views.get_user_announcements),
   

]