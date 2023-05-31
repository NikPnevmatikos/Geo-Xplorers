from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenRefreshView,TokenObtainPairView


urlpatterns = [
   path('login/', views.MyTokenObtainPairView.as_view(), ),
   path('user/', views.MyUserView.as_view()),
   path('locations/',views.LocationsView.as_view()),
   path('locations/<str>',views.SingleLocationView.as_view()),
   path('searches/',views.SearchView.as_view()),
   path('token/refresh/', TokenRefreshView.as_view()),
]