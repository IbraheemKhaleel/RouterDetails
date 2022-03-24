from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('router-details/', RetrieveRouterDetails, name="router-details"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('create-router/', InsertRouterDetails, name="create-router"),
    path('update-router/', UpdateRouterDetails, name="update-router"),
    path('delete-router/', DeleteRouterDetails, name="delete-router"),

]