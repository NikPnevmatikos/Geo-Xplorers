from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenRefreshView,TokenObtainPairView


urlpatterns = [
   path('login/', views.MyTokenObtainPairView.as_view(), ),
   path('user/', views.MyUserView.as_view()),
   path('import/categories/',views.ImportCategories),
   path('import/pois/',views.ImportLocations),

   path('get/locations/', views.get_all_points),
   #path('search/pois/',views.SearchLocationsView.as_view()),
   path('token/refresh/', TokenRefreshView.as_view()),
]